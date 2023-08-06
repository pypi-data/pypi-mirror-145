from typing import Any
from typing import Dict
from typing import Optional

import requests

from httplib2 import Response


class HarvestClient:
    uri = "https://api.harvestapp.com/v2/"

    def __init__(self, app_name: str, account_id: str, token: str) -> None:
        self._headers = {
            "Authorization": f"Bearer {token}",
            "Harvest-Account-ID": account_id,
            "Content-Type": "application/json",
            "User-Agent": app_name,
        }

        response = self.get("users/me.json")
        if response.status_code != 200:
            raise AttributeError(
                f"Failed to authenticate with Harvest API ({response.status_code}):"
                f" {response.text}"
            )

        self._user = response.json()

    @property
    def user(self) -> str:
        return self._user.get("last_name") + ", " + self._user.get("first_name")

    @property
    def short_user(self) -> str:
        return self._user.get("first_name")[0] + self._user.get("last_name")

    @property
    def user_email(self) -> str:
        return self._user.get("email", "Unknown")

    def full_uri(self, endpoint: str) -> str:
        return f"{self.uri}{endpoint}"

    def get(self, endpoint: str) -> Response:
        uri = self.full_uri(endpoint)

        return requests.get(uri, headers=self._headers)

    def post(self, endpoint: str, js: Dict[str, Any]) -> Response:
        uri = self.full_uri(endpoint)

        return requests.post(uri, json=js, headers=self._headers)

    def project_assignments(self) -> Response:
        return self.get("users/me/project_assignments")

    def entries(self, start: str, end: Optional[str] = None) -> Response:
        body = {"from": start, "to": end or start}
        return self.get("time_entries", body)

    def create_entry(
        self, project: int, task: int, spent_date: str, hours: float
    ) -> Response:
        body = {
            "project_id": project,
            "task_id": task,
            "spent_date": spent_date,
            "hours": hours,
        }
        return self.get("time_entries", body)

    def update_entry(self, entry: int, hours: float) -> Response:
        body = {"hours": hours}
        return self.post(f"time_entries/{entry}", body)
