from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

from wheat.calendar.attendee import Attendee
from pendulum import datetime


@dataclass
class Event:
    name: str
    creator: Attendee
    start: datetime
    end: datetime
    attendees: List[Attendee]
    labels: Dict[str, str]
    zoom_link: Optional[str] = "None Found"

    @property
    def date(self) -> str:
        """The date that the event takes place."""
        return self.start.to_date_string()

    @property
    def duration(self) -> float:
        """The event duration in hours."""
        minutes = (self.end - self.start).in_minutes()
        return minutes / 60.0

    @property
    def day(self) -> int:
        """The integer day of the month that the event occurs."""
        return self.start.day

    def __lt__(self, other: "Event") -> bool:
        return self.start <= other.start

    def __str__(self) -> str:
        # Sort the attendees by acceptance status, and
        # space any attendees after the first to create
        # a column that displays nicely in the terminal.
        # This sort method is consistent with the google
        # calendar interface.
        attendees = map(str, sorted(self.attendees))
        attendees = "\n              ".join(attendees)
        pretty_event = (
            f"Meeting Name: {self.name}\n"
            f"Creator:      {self.creator.email}\n"
            f"Starts At:    {self.start}\n"
            f"Ends At:      {self.end}\n"
            f"Attendees:    {attendees}\n"
            f"Zoom Link:    {self.zoom_link}\n"
        )

        return pretty_event
