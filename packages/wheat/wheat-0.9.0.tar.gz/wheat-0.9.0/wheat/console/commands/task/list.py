from typing import Any
from typing import Dict
from typing import List

from cleo.helpers import argument
from cleo.helpers import option
from wheat.console.commands.command import Command
from wheat.harvest.projects.project import Project


class TaskListCommand(Command):

    name = "task list"

    description = "Displays <c1>tasks</c1>."

    arguments = [
        argument("client", "The name of a particular client to show.", optional=True)
    ]

    options = [option("active", "a", description="Only show active projects", flag=True)]

    help = """\
<i>List your <c1>tasks</c1>.

This command allows you to track which <c1>tasks</c1> you are working on.

When you are planning to log hours for a certain Client Project, you should:
  1. use the <c1>task</c1> commands to activate all of the <c1>tasks</c1> you are working on.
  2. use the <c2>log</c2> command to log your hours.

Listing all tasks:

  wheat task list

      National American Space Agency
        Apollo 13
          <success>* (7e24e) Design</success>
          (a2d9c) Launch
      Klingons
        Conquer Puny Souls
          (dbed8) Invade
          (777ef) Conquer

Listing tasks under a certain client:

  wheat task list "Klingons"

      Klingons
        Conquer Puny Souls
          (dbed8) Invade
          (777ef) Conquer

Listing only active tasks:

  wheat task list --active

      National American Space Agency
        Apollo 13
          <success>* (7e24e) Design</success>
"""

    def handle(self) -> int:
        harvest = self.harvest

        clients = harvest.projects.all()

        client = self.argument("client")
        if client:
            if client in clients:
                self.print_clients({client: clients[client]})
                return 0
            else:
                self.line(f'No known clients are named "{client}".', "e")

                self.line("")
                self.line("Client List", "i")
                for client in clients.keys():
                    self.line(f"  {client}")

                self.line("")
                self.line("Ensure that you are enclosing your client name in quotations.")
                return 1

        self.print_clients(clients)

        return 0

    def print_clients(self, clients: Dict[str, Any]) -> int:
        if not self.option("active"):
            for client, projects in clients.items():
                self.pretty_print_client(client, projects)

            return 0

        inactive_clients = []
        for client, projects in clients.items():
            inactive = self.pretty_print_active_client(client, projects)
            if inactive and isinstance(inactive, str):
                inactive_clients.append(inactive)

        if len(inactive_clients) > 0:
            self.line("Inactive clients:")
            self.line('  (use "wheat task list" to view avaliable project tasks)')
            self.line('  (use "wheat task activate <task id>" to set a task as active)')
            for inactive in inactive_clients:
                self.line(f"      {inactive}", "e")

        return 0

    def pretty_print_client(self, client: str, projects: List[Project]) -> None:
        if self.option("active"):
            return self.pretty_print_active_client(client, projects)

        self.line(client)
        for project in projects:
            self.line(f"  {project.name}")
            for task in project.tasks:
                if task.active:
                    self.line(f"    * ({task.short}) {task.name}", style="success")
                else:
                    self.line(f"    ({task.short}) {task.name}", style="i")

        self.line("")
        return 0

    def pretty_print_active_client(self, client: str, projects: List[Project]) -> None:
        active_projects = []

        for project in projects:
            if any(task.active for task in project.tasks):
                active_projects.append(project)

        if len(active_projects) == 0:
            return client

        self.line(client)
        for project in active_projects:
            self.line(f"  {project.name}")
            for task in project.tasks:
                if task.active:
                    self.line(f"    ({task.short}) {task.name}", "success")

        self.line("")
        return 0
