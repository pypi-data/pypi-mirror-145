from pathlib import Path
from typing import Any
from typing import Dict

import yaml


class YAMLFile:
    def __init__(self, path: Path) -> None:
        self._path = path

    @property
    def path(self):
        return self._path

    def exists(self):
        return self._path.exists()

    def touch(self, mode: int = 0o600) -> None:
        self._path.touch(mode=mode)

    def read(self) -> Dict[str, Any]:
        with self._path.open("r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    def write(self, data: Dict[str, Any]) -> None:
        with self._path.open("w", encoding="utf-8") as f:
            yaml.dump(data, f)
