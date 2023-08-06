import sys

from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List

from cleo.commands.command import Command as BaseCommand
from pendulum.datetime import DateTime
from wheat.calendar.calendar import Calendar
from wheat.factory import Factory
from wheat.harvest.harvest import Harvest
from wheat.harvest.projects.task import Task
from wheat.harvest.time_entry import TimeEntry


if TYPE_CHECKING:
    from wheat.console.application import Application


class Command(BaseCommand):
    _harvest = None
    _calendar = None
    _service = None

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

    @property
    def service(self) -> Any:
        if self._service is None:
            self._service = Factory(self.io).create_google_calendar_service()

        return self._service

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

    def active_tasks(self) -> List[tuple]:
        clients = self.harvest.projects.all()

        tasks = []
        for client, projects in clients.items():
            for project in projects:
                for task in project.tasks:
                    if task.active:
                        active = f"{client} <{project.name}, {task.name}>"
                        tasks.append((client, project.id, task.id, active, task.short))

        help = (
            '  (use "wheat task list" to view avaliable tasks)',
            '  (use "wheat task activate <task id>" to set a task as active)',
        )

        if tasks == []:
            self.line("No active tasks found.", "e")
            self.line(help)
            return []

        self.line(f"You have {len(tasks)} active <c1>tasks</c1>.")
        self.line(help)
        self.line("")

        return tasks
