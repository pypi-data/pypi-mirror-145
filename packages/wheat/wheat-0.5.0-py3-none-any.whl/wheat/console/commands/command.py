from typing import TYPE_CHECKING

from cleo.commands.command import Command as BaseCommand


if TYPE_CHECKING:
    from wheat.console.application import Application


class Command(BaseCommand):
    def get_application(self) -> "Application":
        return self.application
