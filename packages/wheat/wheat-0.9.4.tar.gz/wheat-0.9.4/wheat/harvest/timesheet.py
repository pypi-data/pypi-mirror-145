from typing import TYPE_CHECKING
from typing import List

from httplib2 import Response
from pendulum.datetime import DateTime
from wheat.harvest.time_entry import TimeEntry


if TYPE_CHECKING:
    from wheat.harvest.harvest_client import HarvestClient


class Timesheet:
    def __init__(self, client: "HarvestClient") -> None:
        self._client = client

    @property
    def api(self) -> "HarvestClient":
        return self._client

    def fmt_date(self, date: DateTime) -> str:
        return date.format("YYYY-MM-DD")

    def day(self, date: DateTime) -> List[TimeEntry]:
        date = self.fmt_date(date)

        response = self.api.entries(date).json()
        return [TimeEntry(entry) for entry in response["time_entries"]]

    def week(self, start: DateTime, end: DateTime) -> List[TimeEntry]:
        start = self.fmt_date(start)
        end = self.fmt_date(end)

        response = self.api.entries(start, end).json()
        return [TimeEntry(entry) for entry in response["time_entries"]]

    def set_hours(
        self,
        client: str,
        project: int,
        task: int,
        day: DateTime,
        entries: List[TimeEntry],
        hours: float,
    ) -> TimeEntry:
        api = self.api

        # If theres already an entry on this day, update it.
        for entry in entries:
            if entry.check(client, project, task):
                return api.update_entry(entry.id, hours=hours)

        # If we cant find an entry on this day, create one.
        return api.create_entry(project, task, self.fmt_date(day), hours)
