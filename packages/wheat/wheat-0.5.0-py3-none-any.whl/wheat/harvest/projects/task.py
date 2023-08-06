from typing import Any
from typing import Dict
from typing import Optional


class Task:
    def __init__(
        self, name: str, id: str, short: str, active: Optional[bool] = False
    ) -> None:
        self._name = name
        self._id = id
        self._short = short
        self._active = active

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    @property
    def short(self) -> str:
        return self._short

    @property
    def active(self) -> bool:
        return self._active

    def activate(self) -> None:
        self._active = True

    def sleep(self) -> None:
        self._active = False

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self._name,
            "id": self._id,
            "short": self._short,
            "active": self._active,
        }
