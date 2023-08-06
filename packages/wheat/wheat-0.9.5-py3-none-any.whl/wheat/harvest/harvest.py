from pathlib import Path

from wheat.harvest.harvest_client import HarvestClient
from wheat.harvest.projects.projects import Projects
from wheat.harvest.timesheet import Timesheet
from wheat.locations import CONFIG_DIR
from wheat.utils.yaml_file import YAMLFile


class Harvest:
    def __init__(self, api: HarvestClient) -> None:
        self._api = api

        response = api.project_assignments()
        project_assignments = response.json()["project_assignments"]

        projects = Projects(YAMLFile(Path(CONFIG_DIR) / "projects.yaml"))
        projects.sync(project_assignments=project_assignments)
        self._projects = projects

        self._sheet = Timesheet(api)

    @property
    def api(self) -> HarvestClient:
        return self._api

    @property
    def projects(self) -> Projects:
        return self._projects

    @property
    def sheet(self) -> Timesheet:
        return self._sheet
