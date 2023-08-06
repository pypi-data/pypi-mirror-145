from rich.console import Console

from i8_terminal.commands.screen import screen


@screen.command()
def list() -> None:
    console = Console()
    console.print("The screen list command is not implemented yet!", style="yellow")
