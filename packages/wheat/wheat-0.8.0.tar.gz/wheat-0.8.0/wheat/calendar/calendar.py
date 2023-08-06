from typing import TYPE_CHECKING
from typing import List

import pendulum


if TYPE_CHECKING:
    from pendulum.datetime import DateTime
    from wheat.calendar.event import Event


class Calendar:
    """A container class for events."""

    def __init__(self, events: List["Event"]) -> None:
        self._events = sorted(events)  # Sort by start time

    def upcoming_events(self, n: int = 1) -> List["Event"]:
        """Returns the next n events."""
        events = self._events

        now = pendulum.now()
        for index, event in enumerate(events):
            if event.start >= now:
                end = min(index + n, len(events))
                return events[index:end]

        return []

    def events_between(self, start: "DateTime", end: "DateTime") -> List[str]:
        """Yields all events between start and end."""
        events = self._events

        events_between = []
        for event in events:
            if event.start >= start and event.end <= end:
                events_between.append(event)

        return events_between
