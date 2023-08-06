from pathlib import Path
from typing import Any
from typing import Optional
from typing import Tuple

import pendulum

from cleo.io.io import IO
from tomlkit.toml_file import TOMLFile
from wheat.__version__ import __version__
from wheat.calendar.calendar import Calendar
from wheat.calendar.google import create_google_calendar_service
from wheat.calendar.google import get_events_in_interval
from wheat.harvest.harvest import Harvest
from wheat.harvest.harvest_client import HarvestClient
from wheat.locations import CONFIG_DIR


class Factory:
    def __init__(self, io: IO) -> None:
        self.io = io

    def create_google_calendar(self, service: Optional[Any] = None) -> Calendar:
        if service is None:
            service = create_google_calendar_service()

        now = pendulum.now()
        start = now.first_of("month").to_iso8601_string()
        end = now.last_of("month").to_iso8601_string()
        return Calendar(get_events_in_interval(service, start, end))

    def create_harvest(self, api: Optional[HarvestClient] = None) -> Optional[Harvest]:
        if api is not None:
            return Harvest(api)

        id, token = self.harvest_credentials()
        if not (id and token):
            return None

        api = HarvestClient(f"Wheat/{__version__}", id, token)

        return Harvest(api)

    def harvest_credentials(self) -> Optional[Tuple[str, str]]:
        path = Path(CONFIG_DIR) / "harvest_credentials.toml"

        if not path.exists() or not path.is_file():
            return None, None

        credentials = TOMLFile(path).read().get("credentials", {})

        id = credentials.get("account_id")
        token = credentials.get("token")
        if id is None or token is None:
            return None, None

        return id, token

    def create_harvest_credentials(self, account_id: str, token: str) -> Path:
        path = Path(CONFIG_DIR) / "harvest_credentials.toml"

        if not path.exists():
            mode = 0o600  # Ensure only user can access the file.
            path.touch(mode=mode)

        template = f'[credentials]\naccount_id = "{account_id}"\ntoken = "{token}"\n'

        path.write_text(template)

        return path
