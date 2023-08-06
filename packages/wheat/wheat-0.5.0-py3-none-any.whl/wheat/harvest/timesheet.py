from typing import TYPE_CHECKING
from typing import List

from wheat.harvest.time_entry import TimeEntry
from httplib2 import Response
from pendulum import datetime


if TYPE_CHECKING:
    from wheat.harvest.harvest_client import HarvestClient


class Timesheet:
    def __init__(self, client: "HarvestClient") -> None:
        self._client = client

    @property
    def api(self) -> "HarvestClient":
        return self._client

    def fmt_date(self, date: datetime) -> str:
        return date.format("YYYY-MM-DD")

    def day(self, date: datetime) -> List[TimeEntry]:
        date = self.fmt_date(date)

        return [TimeEntry(entry) for entry in self.api.entries(date)]

    def set_hours(
        self, client: int, project: int, task: int, day: int, hours: float
    ) -> Response:
        api = self.api

        # If theres already an entry on this day, update it.
        for entry in self.day(day):
            if entry.check(client, project, task):
                return api.update_entry(entry.id, hours=hours)

        # If we cant find an entry on this day, create one.
        return api.create_entry(project, task, self.fmt_date(day), hours)
