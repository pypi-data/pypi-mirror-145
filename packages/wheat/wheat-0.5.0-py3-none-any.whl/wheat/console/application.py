from importlib import import_module
from typing import Callable
from typing import Optional
from typing import Union

from cleo.application import Application as BaseApplication
from cleo.formatters.style import Style
from cleo.io.inputs.input import Input
from cleo.io.io import IO
from cleo.io.outputs.output import Output
from wheat.__version__ import __version__
from wheat.console.command_loader import CommandLoader
from wheat.console.commands.command import Command


def load_command(name: str) -> Callable:
    def _load() -> type[Command]:
        words = name.split(" ")
        module = import_module("wheat.console.commands." + ".".join(words))
        command_class = getattr(module, "".join(c.title() for c in words) + "Command")
        return command_class()

    return _load


COMMANDS = ["about", "auth"]


class Application(BaseApplication):
    def __init__(self) -> None:
        super().__init__("wheat", __version__)

        self._io: Union[IO, None] = None

        command_loader = CommandLoader({name: load_command(name) for name in COMMANDS})
        self.set_command_loader(command_loader)

    @property
    def command_loader(self) -> CommandLoader:
        return self._command_loader

    def create_io(
        self,
        input: Optional[Input] = None,
        output: Optional[Output] = None,
        error_output: Optional[Output] = None,
    ) -> IO:
        io = super().create_io(input, output, error_output)

        # Set our own CLI styles
        formatter = io.output.formatter
        formatter.set_style("c1", Style("blue"))
        formatter.set_style("c2", Style("magenta"))

        formatter.set_style("e", Style("red", options=["bold"]))
        formatter.set_style("w", Style("yellow", options=["bold"]))
        formatter.set_style("i", Style("default", options=["bold"]))

        formatter.set_style("success", Style("green", options=["bold"]))
        formatter.set_style("question", Style("blue"))
        io.output.set_formatter(formatter)
        io.error_output.set_formatter(formatter)

        self._io = io

        return io


def main() -> int:
    return Application().run()


if __name__ == "__main__":
    main()
