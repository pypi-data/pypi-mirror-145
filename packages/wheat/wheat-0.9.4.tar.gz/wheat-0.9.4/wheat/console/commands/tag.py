from typing import Any
from typing import List
from typing import Tuple

import pendulum

from cleo.helpers import option
from pendulum.datetime import DateTime
from wheat.calendar.event import Event
from wheat.calendar.google import patch_event
from wheat.console.commands.command import Command
from wheat.factory import Factory
from wheat.utils.time import month_normalizer


class TagCommand(Command):

    name = "tag"

    description = (
        "Tags meetings in a given interval with an associated project <c1>task</c1>."
    )

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

    def handle(self) -> int:
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
        factory = Factory(self.io)
        service = factory.create_google_calendar_service()
        calendar = factory.create_google_calendar(service, dates[0], dates[-1])

        tasks = self.active_tasks()
        for date in dates:
            events = calendar.events_between(date.start_of("day"), date.end_of("day"))

            pretty_date = date.format("dddd [the] Do")
            self.line(f"Tagging events on {pretty_date}:")
            self.line(f"  (you have <w>{len(events)}</w> calendar events to tag)")

            self.tag_events(service, tasks, events)

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

    def tag_events(self, service: Any, tasks: List[Tuple], events: List[Event]) -> None:
        for event in events:
            if event.tagged:
                continue

            for ln in event.compact():
                self.line(ln)

            if self.io.is_interactive():
                self.line("")

            task_choices = [str(task[3]) for task in tasks] + ["None"]
            associated = self.choice(
                "Task to associate", choices=task_choices, attempts=3
            )

            if associated is not False and associated != "None":
                for task in tasks:
                    tag_id = str(task[3])
                    if tag_id == associated:
                        patch_event(
                            service, event.id, {"short": str(task[4]), "id": tag_id}
                        )

                        self.line("")
                        self.line(f"  {event.name} tagged <success>✔️</success>")
                        self.line("")
