from cleo.helpers import argument
from wheat.console.commands.command import Command


class TaskSleepCommand(Command):

    name = "task sleep"

    description = "Puts a <c1>task</c1> to sleep."

    arguments = [argument("Task ID", "The short tag of the Task.", optional=False)]

    help = """\
<i>Put a <c1>Task</c1> to sleep, hiding it when using the <c1>log</c1> command.

Usage Example:
  1. use "wheat task list" to see all of your avaliable <c1>Tasks</c1>.

    ~ (Example <c1>Task</c1> List) ~

    National American Space Agency
      Apollo 13
        (7e24e) Design
        <success>* (a2d9c) Launch</success>

  2. use "wheat task sleep a2d9c" to sleep the Apollo 13 "Launch" <c1>Task</c1>.
  3. use "wheat task list" again to view your changes:

    ~ (Example <c1>Task</c1> List) ~

    National American Space Agency
      Apollo 13
        (7e24e) Design
        (a2d9c) Launch
"""

    def handle(self) -> int:
        harvest = self.harvest

        task_id = self.argument("Task ID")

        slept_task = harvest.projects.sleep(task_id)
        if slept_task and isinstance(slept_task, str):
            self.line(f'No tasks with ID "{task_id}" found.', "e")
            return 1

        self.line(f"Slept Task {slept_task.short}.", "success")
