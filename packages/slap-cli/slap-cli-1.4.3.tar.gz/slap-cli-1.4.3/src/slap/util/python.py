
import dataclasses
import importlib
import functools
import json
import os
import pkg_resources
import subprocess as sp
import textwrap
import typing as t
from pathlib import Path


class Pep517BuildBackend:
  """ A wrapper around a [PEP 517][] build backend.

    [PEP 517]: https://www.python.org/dev/peps/pep-0517/
  """

  class _InternalBackend:
    def build_sdist(self, sdist_directory: str, config_settings: dict | None) -> str: ...
    def build_wheel(self, wheel_directory: str, config_settings: dict | None, metadata_directory:  str | None = None) -> str: ...

  _module: _InternalBackend

  def __init__(self, name: str, project_directory: Path, build_directory: Path) -> None:
    self.name = name
    self.project_directory = project_directory.resolve()
    self.build_directory = build_directory.resolve()
    self._module = t.cast(t.Any, importlib.import_module(name))

  def __repr__(self) -> str:
    return f'BuildBackend("{self.name}")'

  def build_sdist(self, config_settings: dict[str, str | list[str]] | None = None) -> Path:
    old_cwd = Path.cwd()
    try:
      os.chdir(self.project_directory)
      filename = self._module.build_sdist(str(self.build_directory), config_settings)
      return self.build_directory / filename
    finally:
      os.chdir(old_cwd)

  def build_wheel(self, config_settings: dict[str, str | list[str]] | None = None) -> Path:
    old_cwd = Path.cwd()
    try:
      os.chdir(self.project_directory)
      filename = self._module.build_wheel(str(self.build_directory), config_settings, None)
      return self.build_directory / filename
    finally:
      os.chdir(old_cwd)


@dataclasses.dataclass
class Environment:
  executable: str
  version: str
  platform: str
  prefix: str
  base_prefix: str | None
  real_prefix: str | None

  def is_venv(self) -> bool:
    return bool(self.real_prefix or (self.base_prefix and self.prefix != self.base_prefix))

  @staticmethod
  @functools.lru_cache()
  def of(python: str | t.Sequence[str]) -> 'Environment':
    code = textwrap.dedent('''
      import sys, platform, json
      print(json.dumps({
        "executable": sys.executable,
        "version": sys.version,
        "platform": platform.platform(),
        "prefix": sys.prefix,
        "base_prefix": getattr(sys, 'base_prefix', None),
        "real_prefix": getattr(sys, 'real_prefix', None),
      }))
    ''')
    if isinstance(python, str):
      python = [python]
    return Environment(**json.loads(sp.check_output(list(python) + ['-c', code]).decode()))

  def get_distribution(self, distribution: str) -> pkg_resources.Distribution | None:
    return self.get_distributions([distribution])[distribution]

  def get_distributions(self, distributions: t.Collection[str]) -> dict[str, pkg_resources.Distribution | None]:
    import pickle
    code = textwrap.dedent('''
      import sys, pkg_resources, pickle
      result = []
      for arg in sys.argv[1:]:
        try:
          dist = pkg_resources.get_distribution(arg)
        except pkg_resources.DistributionNotFound:
          dist = None
        result.append(dist  )
      sys.stdout.buffer.write(pickle.dumps(result))
    ''')
    keys = list(distributions)
    result = pickle.loads(sp.check_output([self.executable, '-c', code] + keys))
    return dict(zip(keys, result))
