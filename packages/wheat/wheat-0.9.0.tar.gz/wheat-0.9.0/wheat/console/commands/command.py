import sys

from typing import TYPE_CHECKING
from typing import List

from cleo.commands.command import Command as BaseCommand
from pendulum.datetime import DateTime
from wheat.calendar.calendar import Calendar
from wheat.factory import Factory
from wheat.harvest.harvest import Harvest
from wheat.harvest.time_entry import TimeEntry


if TYPE_CHECKING:
    from wheat.console.application import Application


class Command(BaseCommand):
    _harvest = None
    _calendar = None

    @property
    def harvest(self) -> Harvest:
        if self._harvest is None:
            try:
                self._harvest = Factory(self.io).create_harvest()
            except AttributeError:
                self.line_error(
                    'You must authenticate with Harvest via "wheat auth" before you can'
                    " use this command."
                )
                sys.exit(1)

        return self._harvest

    @property
    def calendar(self) -> Calendar:
        if self._calendar is None:
            self._calendar = Factory(self.io).create_google_calendar()

        return self._calendar

    def get_application(self) -> "Application":
        return self.application

    def pretty_print_date(self, date: DateTime, entries: List[TimeEntry]) -> None:
        clients = {}
        for entry in entries:
            client = entry.client.name
            project = entry.project.name
            task = entry.task.name

            id = f"{client} <{project}, {task}>"
            if id not in clients:
                clients[id] = 0

            clients[id] += entry.hours

        total = sum(clients.values())

        if total == 0:
            return

        clients = dict(sorted(clients.items(), key=lambda x: x[1], reverse=True))

        for client, hours in clients.items():
            self.line(f"    {client}: {hours} <success>✔️</success>")
