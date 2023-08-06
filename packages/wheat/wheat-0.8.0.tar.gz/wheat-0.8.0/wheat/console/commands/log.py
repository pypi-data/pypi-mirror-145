from asyncio import Task
from typing import Any
from typing import Dict
from typing import List

import pendulum

from cleo.helpers import option
from pendulum.datetime import DateTime
from wheat.console.commands.command import Command
from wheat.harvest.projects.project import Project
from wheat.harvest.time_entry import TimeEntry
from wheat.utils.time import month_normalizer


class LogCommand(Command):

    name = "log"

    description = "Log hours in <c1>Harvest</c1>."

    now = pendulum.now()
    options = [
        option(
            "week",
            "w",
            description=(
                "Log hours for a particular week of the month. (current week by default)."
            ),
            flag=False,
            default=now.week_of_month,
        ),
        option(
            "month",
            "m",
            description="Log hours for a particular month. (current month by default).",
            flag=False,
            default=now.month,
        ),
        option(
            "year",
            "y",
            description="Log hours for a particular year. (current year by default).",
            flag=False,
            default=now.year,
        ),
        option(
            "start",
            "s",
            description=(
                "The start date of an interval. Must also provide an end. (YYYY/MM/DD)"
            ),
            flag=False,
        ),
        option(
            "end",
            "e",
            description=(
                "The end date of an interval. Must also provide a start. (YYYY/MM/DD)"
            ),
            flag=False,
        ),
    ]

    help = """\
By default, the <c1>log</c1> command will log task hours for the current week.

<w>The log command will only let you enter hours for tasks that you have activated via "wheat task activate <task id>". </w>

Examples:

  1. Log time for each day between the 14th and 17th day of April, 2021: "wheat log --start 2021/04/14 --end 2021/04/17"

  2. Log time for the first week of April, 2021: "wheat log -w 1 -y 2021 -m 4"
      (you can also pass strings for the month: "wheat log -w 1 -y 2021 -m april")
"""

    def handle(self) -> int:
        self.sheet = self.harvest.sheet

        start = self.option("start")
        end = self.option("end")
        if start and not end or end and not start:
            self.line("You must provide both a start and end date.", "e")
            return 1

        if start and end:
            start = pendulum.parse(start)
            end = pendulum.parse(end)
            dates = self.interval_dates(start, end)
        else:
            year = int(self.option("year"))
            month = month_normalizer(self.option("month"))
            week = int(self.option("week"))

            dates = self.week_dates(year, month, week)

        if isinstance(dates, int):
            return dates  # Exit code 1

        first = dates[0].format("dddd [the] Do")
        last = dates[-1].format("dddd [the] Do")
        self.line(f"Logging hours for {first} -> {last}.")

        self.line("")
        return self.log_hours_for_interval(dates[0], dates[-1])

    def interval_dates(self, start: DateTime, end: DateTime) -> List[DateTime]:
        period = end.diff(start)

        if end < start:
            self.line("The start date must be before the end date.", "e")
            return 1

        return list(period.range("days"))

    def week_dates(self, year: int, month: int, week: int) -> List[DateTime]:
        month = pendulum.datetime(year, month, 1)

        start = month.start_of("week").add(weeks=(week - 1))
        end = start.add(weeks=1)

        return self.interval_dates(start, end)

    def log_hours_for_interval(self, start: DateTime, end: DateTime) -> int:
        clients = self.harvest.projects.all()

        tasks = self.extract_active_tasks(clients)
        if tasks == []:
            return 1

        entries = self.sheet.week(start, end)

        new_entries = {}
        for day in pendulum.period(start, end):
            date = day.format("dddd [the] Do")
            self.line(f"Enter task hours for {date} (enter to skip task, 'n' to exit):")
            for task in tasks:
                question = self.create_question(f"  {task[3]}:")
                hours = self.ask(question)

                if hours is None:
                    continue

                if isinstance(hours, str):
                    if hours.lower() == "n":
                        break

                hours = float(hours)

                response = self.sheet.set_hours(
                    str(task[0]), int(task[1]), int(task[2]), day, entries, hours
                )

                entry = TimeEntry(response.json())

                if date not in new_entries:
                    new_entries[date] = []

                new_entries[date].append(entry)

            self.line("")
            self.line(f"  {date} Synced <success>✔️</success>")

            if new_entries.get(date, []) != []:
                self.pretty_print_date(date, new_entries[date])

            self.line("")
            if isinstance(hours, str):
                if hours.lower() == "n":
                    break

        self.line(f"Hours logged. Well done {self.harvest.api.first_name}! :)", "success")
        return 0

    def extract_active_tasks(self, clients: Dict[str, Any]) -> List[Task]:
        tasks = []
        for client, projects in clients.items():
            for project in projects:
                for task in project.tasks:
                    if task.active:
                        active = f"{client} <{project.name}, {task.name}>"
                        tasks.append((client, project.id, task.id, active))

        help = (
            '  (use "wheat task list" to view avaliable tasks)',
            '  (use "wheat task activate <task id>" to set a task as active)',
        )

        if tasks == []:
            self.line("No active tasks found.", "e")
            self.line(help)
            return 1

        self.line(f"You have {len(tasks)} active <c1>tasks</c1>.")
        self.line(help)
        self.line("")
        return tasks
