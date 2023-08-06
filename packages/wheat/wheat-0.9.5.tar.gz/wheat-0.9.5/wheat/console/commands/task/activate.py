from cleo.helpers import argument
from wheat.console.commands.command import Command


class TaskActivateCommand(Command):

    name = "task activate"

    description = "Activates a <c1>task</c1>."

    arguments = [
        argument(
            "Task ID",
            "The short tag of the <c1>Task</c1>.",
            optional=False,
            multiple=True,
        )
    ]

    help = """\
<i>Activate a <c1>Task</c1>, causing it to appear when using the <c1>log</c1> command.

Usage Example:
  1. use "wheat task list" to see all of your avaliable <c1>Tasks</c1>.

    ~ (Example <c1>Task</c1> List) ~

    National American Space Agency
      Apollo 13
        (7e24e) Design
        (a2d9c) Launch

  2. use "wheat task activate a2d9c" to activate the Apollo 13 "Launch" <c1>Task</c1>.
  3. use "wheat task list" again to view your changes:

    ~ (Example <c1>Task</c1> List) ~

    National American Space Agency
      Apollo 13
        (7e24e) Design
        <success>* (a2d9c) Launch</success></i>
"""

    def handle(self) -> int:
        harvest = self.harvest

        task_ids = self.argument("Task ID")
        for task_id in task_ids:
            activated_task = harvest.projects.activate(task_id)
            if activated_task and isinstance(activated_task, str):
                self.line(f'No tasks with ID "{task_id}" found.', "e")
                return 1

            self.line(f"Activated Task {activated_task.short}.", "success")
