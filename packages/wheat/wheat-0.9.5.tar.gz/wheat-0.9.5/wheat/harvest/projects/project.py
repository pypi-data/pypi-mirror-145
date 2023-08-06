from typing import Any
from typing import Dict
from typing import List
from typing import Optional

from wheat.harvest.projects.task import Task
from wheat.utils.hash import hash


class Project:
    def __init__(self, name: str, id: str, tasks: List[Dict[str, Any]]) -> None:
        self._name = name
        self._id = str(id)

        self.tasks = []
        for task in tasks:
            short = hash(str(id) + str(task["id"]))
            task["short"] = task.get("short", short)
            self.tasks.append(Task(**task))

    @property
    def name(self) -> str:
        return self._name

    @property
    def id(self) -> str:
        return self._id

    def merge(self, other: "Project") -> None:
        for task in self.tasks:
            other_task = other.get_task(task.short)
            if other_task is not None:
                if task.active or other_task.active:
                    task.activate()
                else:
                    task.sleep()

    def has(self, short: str) -> bool:
        return any(task.short == short for task in self.tasks)

    def get_task(self, short: str) -> Task:
        for task in self.tasks:
            if task.short == short:
                return task

    def as_dict(self) -> Dict[str, Any]:
        return {
            "name": self._name,
            "id": self._id,
            "tasks": [task.as_dict() for task in self.tasks],
        }

    def __eq__(self, other: "Project") -> bool:
        return self.name == other.name and self.id == other.id
