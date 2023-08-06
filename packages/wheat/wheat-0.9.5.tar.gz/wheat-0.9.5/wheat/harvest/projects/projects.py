from contextlib import contextmanager
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple

from wheat.harvest.projects.project import Project
from wheat.harvest.projects.task import Task
from wheat.utils.yaml_file import YAMLFile


class Projects:
    def __init__(self, file: "YAMLFile") -> None:
        self._file = file

    @property
    def file(self) -> YAMLFile:
        return self._file

    def all(self) -> Dict[str, Any]:
        with self.secure() as project_config:
            clients = self.clients(project_config)

        return clients

    def clients(self, config: Dict[str, Any]) -> Dict[str, Any]:
        clients = {}
        for client in config["clients"]:
            clients[client["name"]] = self.process(client)

        return clients

    def process(self, client: Dict[str, Any]) -> List[Project]:
        projects = []
        for project in client["projects"]:
            projects.append(Project(**project))

        return projects

    def compact(self, clients: Dict[str, Any]) -> Dict[str, Any]:
        final = []
        for client, projects in clients.items():
            projects = [project.as_dict() for project in projects]

            final.append({"name": client, "projects": projects})

        return final

    def sync(self, project_assignments: List[Dict[str, Any]]) -> None:
        with self.secure() as project_config:
            current_projects = self.clients(project_config)

            actual_projects = {}
            for assignment in project_assignments:
                client = assignment["client"]["name"]

                if client not in actual_projects:
                    actual_projects[client] = []

                name = assignment["project"]["name"]
                id = str(assignment["project"]["id"])
                tasks = [assign["task"] for assign in assignment["task_assignments"]]

                actual_projects[client].append(Project(name, id, tasks))

            new_projects = {}
            for client, projects in actual_projects.items():
                # If we are currently missing a client, add it.
                if client not in new_projects:
                    new_projects[client] = []

                # If we are currently missing a project, add it.
                for project in projects:
                    # If the project exists in our config already, make sure we
                    # retain the status of its tasks when syncing.
                    if client in current_projects and project in current_projects[client]:
                        for curr_proj in current_projects[client]:
                            if curr_proj == project:
                                project.merge(curr_proj)

                    if project not in new_projects[client]:
                        new_projects[client].append(project)

            project_config["clients"] = self.compact(new_projects)

    def activate(self, task_id: str) -> Task:
        with self.secure() as project_config:
            current_projects = self.clients(project_config)

            activated_task = None
            for _, projects in current_projects.items():
                for project in projects:
                    task = project.get_task(task_id)
                    if task and isinstance(task, Task):
                        task.activate()
                        activated_task = task
                        break

            project_config["clients"] = self.compact(current_projects)

        return activated_task or f"Failed to locate a task with id: {task_id}."

    def sleep(self, task_id: str) -> str:
        with self.secure() as project_config:
            current_projects = self.clients(project_config)

            activated_task = None
            for _, projects in current_projects.items():
                for project in projects:
                    task = project.get_task(task_id)
                    if task and isinstance(task, Task):
                        task.sleep()
                        activated_task = task
                        break

            project_config["clients"] = self.compact(current_projects)

        return activated_task or f"Failed to locate a task with id: {task_id}."

    @contextmanager
    def secure(self) -> Dict[str, Any]:
        if self.file.exists():
            initial_config = self.file.read()
            config = self.file.read()
        else:
            initial_config = {"clients": []}
            config = {"clients": []}

        new_file = not self.file.exists()

        yield config

        try:
            # Ensuring the file is only readable and writable
            # by the current user
            mode = 0o600

            if new_file:
                self.file.touch(mode=mode)

            self.file.write(config)
        except Exception:
            self.file.write(initial_config)

            raise
