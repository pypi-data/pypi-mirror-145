from typing import List

import pendulum

from cleo.helpers import option
from pendulum.datetime import DateTime
from wheat.console.commands.command import Command
from wheat.harvest.time_entry import TimeEntry
from wheat.utils.time import month_normalizer


class ViewCommand(Command):

    name = "view"

    description = "Displays logged hours for a time period."

    now = pendulum.now()

    options = [
        option(
            "week",
            "w",
            description="Show a particular week of the month. (current week by default).",
            flag=False,
            default=now.week_of_month,
        ),
        option(
            "month",
            "m",
            description="Show a particular month. (current month by default).",
            flag=False,
            default=now.month,
        ),
        option(
            "year",
            "y",
            description="Show a particular year. (current year by default).",
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
By default, the <c1>view</c1> command displays all logged hours for the current week.

Examples:

  1. View the 14th to the 17th day of April, 2021: "wheat view --start 2021/04/14 --end 2021/04/17"

  2. View the first week of April, 2021: "wheat view -w 1 -y 2021 -m 4"
      (you can also pass strings for the month: "wheat view -w 1 -y 2021 -m april")
"""

    def handle(self) -> int:
        self.sheet = self.harvest.sheet
        self.hours_total = 0

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
        self.line(f"Viewing hours logged for {first} -> {last}.")

        self.line("")
        self.pretty_print_week(dates[0], dates[-1])

        self.line(f"Total hours: {self.hours_total}")
        return 0

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

    def pretty_print_week(self, start: DateTime, end: DateTime) -> None:
        entries = self.sheet.week(start, end)
        entries.reverse()  # Sort ascending by date.

        weeks_entries = {}

        for entry in entries:
            date = pendulum.parse(entry.date).format("dddd [the] Do")
            if date not in weeks_entries:
                weeks_entries[date] = []

            weeks_entries[date].append(entry)

        for date, entries in weeks_entries.items():
            self.pretty_print_date(date, entries)

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
            self.hours_total += entry.hours

        total = sum(clients.values())

        if total == 0:
            return

        clients = dict(sorted(clients.items(), key=lambda x: x[1], reverse=True))

        self.line(date)
        for client, hours in clients.items():
            self.line(f"  {hours}: {client}")

        self.line(f"  ---")
        self.line(f"  {total} Total hours")
        self.line("")
