from pathlib import Path
from typing import TYPE_CHECKING
from typing import Any
from typing import Dict
from typing import List

import pendulum

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from wheat.calendar.attendee import Attendee
from wheat.calendar.event import Event
from wheat.locations import CONFIG_DIR
from wheat.utils.zoom import contains_zoom_link


if TYPE_CHECKING:
    from pendulum.datetime import DateTime


def create_google_calendar_service(credentials: Credentials) -> Any:
    """Creates a google calendar service object.

    Args:
        credentials (Credentials): A google credentials object.

    Returns:
        Any: A google calendar service object.
    """
    return build("calendar", "v3", credentials=credentials)


def create_or_find_existing_google_credentials() -> Credentials:
    scopes = ["https://www.googleapis.com/auth/calendar.events"]

    config_dir = Path(CONFIG_DIR)
    if not config_dir.exists():
        config_dir.mkdir(parents=True, exist_ok=True)

    file = config_dir / "credentials.json"
    if not file.exists():
        file.touch(mode=0o600)  # Ensure user is only one with access.

    creds = None

    if file.exists():
        creds = Credentials.from_authorized_user_file(str(file))

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            client_secrets = (
                Path(__file__).parent / "client_credentials" / "credentials.json"
            )
            flow = InstalledAppFlow.from_client_secrets_file(str(client_secrets), scopes)
            creds = flow.run_local_server(port=0)

        # Save the credentials for the next run
        file.write_text(creds.to_json())

    return creds


def get_events_in_interval(
    service: Any, start: "DateTime", end: "DateTime"
) -> List[Event]:
    query = dict(
        calendarId="primary",
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy="startTime",
    )
    query = service.events().list(**query)
    event_descriptions = query.execute().get("items", [])

    return [_process_event_description(desc) for desc in event_descriptions]


def _process_event_description(description: Dict[str, Any]) -> Event:
    """Processes a google calendar event description.

    Expects `descriptions` to contain a dictionary which is returned
    by the google calendar events API.

    Args:
        descriptions (Dict[str, Any]):

    Returns:
        List[Event]: A list of Events which represent the event descriptions.
    """

    def datetime_string(dt: "DateTime", tz: str) -> str:
        """Converts a datetime object to a string."""
        return pendulum.parse(dt, tz=tz)

    start = datetime_string(
        description["start"]["dateTime"], description["start"]["timeZone"]
    )
    end = datetime_string(description["end"]["dateTime"], description["end"]["timeZone"])

    attendees = [
        Attendee(
            attendee.get("email", "Unknown"),
            attendee.get("name", "Unknown"),
            attendee.get("self", False),
            attendee.get("responseStatus", "needsAction"),
        )
        for attendee in description.get("attendees", [])
    ]

    entry_link = None
    for point in description.get("conferenceData", {}).get("entryPoints", []):
        link = contains_zoom_link(point.get("uri", ""))
        if link:
            entry_link = link
            break

    # Look for a zoom link in these four locations, in order.
    # if none is found, use a 'not found' string.
    zoom_link = (
        contains_zoom_link(description.get("location", ""))
        or contains_zoom_link(description.get("description", ""))
        or entry_link
        or "Not Found."
    )

    return Event(
        name=description["summary"],
        creator=Attendee(email=description["creator"].get("email", "Unknown")),
        start=start,
        end=end,
        attendees=attendees,
        labels=description.get("labels", {}),
        zoom_link=zoom_link,
    )
