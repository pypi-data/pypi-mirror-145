from wheat.console.commands.command import Command


class AboutCommand(Command):

    name = "about"

    description = "Shows information about Wheat."

    def handle(self) -> None:
        self.line(f"<c1>Wheat - Time tracking hardwired into your terminal.</c1>")
