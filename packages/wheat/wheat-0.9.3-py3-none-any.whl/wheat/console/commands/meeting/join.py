import webbrowser

from cleo.helpers import argument
from wheat.calendar.event import Event
from wheat.console.commands.command import Command


class MeetingJoinCommand(Command):

    name = "meeting join"

    description = "Join an upcoming <c1>meeting</c1>."

    arguments = [argument("name", "The name of the <c1>meeting</c1>.", optional=True)]

    help = """\
<i>Join an upcoming <c1>meeting</c1>.

If no meeting name is supplied, the first upcoming meeting will be joined.
"""

    def handle(self) -> int:
        calendar = self.calendar

        name = self.argument("name")
        if name is None:
            events = calendar.upcoming_events(1)
            if len(events) == 0:
                self.line("No upcoming meetings.", "e")
                return 1

            self.join(events[0])
            return 0

        event = calendar.event(name)
        if event is None:
            self.line(f"No calendar event found with the name: {name}.", "e")
            return 1

        self.join(event)
        return 0

    def join(self, event: Event) -> None:
        if event.zoom_link == "None Found":
            self.line("No Zoom link found for this meeting.", "e")
            return

        self.line(f"Joining zoom link: {event.zoom_link}")
        webbrowser.open(event.zoom_link)
