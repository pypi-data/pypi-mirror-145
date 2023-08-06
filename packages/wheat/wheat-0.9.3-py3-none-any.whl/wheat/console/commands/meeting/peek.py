from cleo.helpers import argument
from wheat.console.commands.command import Command


class MeetingPeekCommand(Command):

    name = "meeting peek"

    description = "Displays one or more of your upcoming <c1>meetings</c1>."

    arguments = [
        argument(
            "count",
            "The number of <c1>meetings</c1> to display.",
            optional=True,
            default="1",
        )
    ]

    def handle(self) -> int:
        calendar = self.calendar

        count = int(self.argument("count"))
        events = calendar.upcoming_events(count)

        if len(events) == 0:
            self.line("No upcoming meetings.", "e")
            return 1

        self.line(f"Upcoming meeting(s):", "success")
        self.line("")

        for event in events:
            self.line(str(event))

        return 0
