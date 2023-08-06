from ctypes import Union
from dataclasses import dataclass
from typing import Dict
from typing import List
from typing import Optional

from pendulum import datetime
from wheat.calendar.attendee import Attendee


@dataclass
class Event:
    id: str
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

    @property
    def tagged(self) -> bool:
        """True if this event has an associated task short."""
        return self.short and isinstance(self.short, str)

    @property
    def short(self) -> str:
        """The Task short related to this event, if one exists."""
        return self.labels.get("short")

    def compact(self) -> List[str]:
        start = self.start.to_day_datetime_string()
        end = self.end.to_day_datetime_string()
        pretty_event = (
            f"Meeting:      {self.name} - {self.creator.email}",
            f"Creator:      {start} -> {end}",
        )

        return pretty_event

    def __lt__(self, other: "Event") -> bool:
        return self.start <= other.start

    def __str__(self) -> str:
        # Sort the attendees by acceptance status, and
        # space any attendees after the first to create
        # a column that displays nicely in the terminal.
        # This sort method is consistent with the google
        # calendar interface.
        attendees = list(map(str, sorted(self.attendees)))
        if len(attendees) > 7:
            remaining = len(attendees) - 7
            attendees = attendees[:7]
            attendees.append(f"   + {remaining} more.")

        attendees = "\n              ".join(attendees)

        start = self.start.to_day_datetime_string()
        end = self.end.to_day_datetime_string()
        pretty_event = (
            f"Meeting Name: {self.name}\n"
            f"Creator:      {self.creator.email}\n"
            f"Starts At:    {start}\n"
            f"Ends At:      {end}\n"
            f"Attendees:    {attendees}\n"
            f"Zoom Link:    {self.zoom_link}\n"
        )

        return pretty_event
