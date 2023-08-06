from typing import Any
from typing import Dict
from typing import NamedTuple
from typing import Optional


class HarvestClient(NamedTuple):
    """A Harvest Client."""

    id: int
    name: str


class HarvestProject(NamedTuple):
    """A Harvest Project."""

    id: int
    name: str


class HarvestTask(NamedTuple):
    """A Harvest Task."""

    id: int
    name: str


class TimeEntry:
    def __init__(self, entry: Dict[str, Any]) -> None:
        """An object model that matches the Harvest API's time entry object.

        This is modeled after the time_entries endpoint's response model. This object
        assumes you are using the Harvest v2 API, and is not compatible with v1.

        Args:
            entry (Dict[str, Any]): A response returned from the time_entries endpoint.
        """
        self._id = entry["id"]
        self._date = entry["spent_date"]
        self._hours = entry["hours"]
        self._locked = entry["locked"]
        self._locked_reason = entry["locked_reason"]

        self._client = entry["client"]
        self._project = entry["project"]
        self._task = entry["task"]

    @property
    def id(self) -> int:
        """The id of the time entry."""
        return self._id

    @property
    def date(self) -> str:
        """The date of the time entry."""
        return self._date

    @property
    def hours(self) -> float:
        """The amount of hours the entry represents."""
        return self._hours

    @property
    def locked(self) -> bool:
        """If the entry has been locked or not."""
        return self._locked

    @property
    def locked_reason(self) -> Optional[str]:
        """If the entry is locked, this is the reason why. If not, this is null."""
        return self._locked_reason

    @property
    def client(self) -> HarvestClient:
        """The client that the entry is associated with."""
        return HarvestClient(self._client["id"], self._client["name"])

    @property
    def project(self) -> HarvestProject:
        """The project that the entry is associated with."""
        return HarvestProject(self._project["id"], self._project["name"])

    @property
    def task(self) -> HarvestTask:
        """The task that the entry is associated with."""
        return HarvestTask(self._task["id"], self._task["name"])

    def __eq__(self, other: "TimeEntry") -> bool:
        return self.id == other.id

    def check(self, client: int, project: int, task: int) -> bool:
        return (
            self.client.id == client
            and self.project.id == project
            and self.task.id == task
        )
