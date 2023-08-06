from collections import namedtuple
from dataclasses import dataclass
from typing import Tuple


@dataclass
class Attendee:
    email: str
    name: str = "Unknown"
    myself: bool = False
    acceptance_status: str = "needsAction"

    @property
    def status(self) -> Tuple[int, str]:
        """A `namedtuple ('weight': int, 'icon': str)` which represents acceptance status."""
        Status: Tuple[int, str] = namedtuple(
            "Status", ["weight", "icon"], defaults=[5, "🔴"]
        )

        statuses = {
            "accepted": Status(1, "🟢"),
            "tentative": Status(2, "🟡"),
            "needsAction": Status(3, "🟡"),
            "declined": Status(4, "🔴"),
        }

        return statuses.get(self.acceptance_status, Status())

    def __lt__(self, other: "Attendee") -> bool:
        return self.status.weight <= other.status.weight

    def __str__(self) -> str:
        return f"{self.status.icon} {self.email}"
