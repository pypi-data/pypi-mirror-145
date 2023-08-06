# type: ignore[attr-defined]
from enum import Enum

import typer
from rich.console import Console

from drowsy_server import version
from drowsy_server.interface import show_interface


class Color(str, Enum):
    white = "white"
    red = "red"
    cyan = "cyan"
    magenta = "magenta"
    yellow = "yellow"
    green = "green"


app = typer.Typer(
    name="drowsy_server",
    help="Drowsy Server",
    add_completion=True,
)
console = Console()


def version_callback(print_version: bool) -> None:
    """Print the version of the package."""
    if print_version:
        console.print(f"[red]drowsy_server[/] version: [bold blue]{version}[/]")
        raise typer.Exit()


@app.command(name="")
def main(
    print_version: bool = typer.Option(
        None,
        "-v",
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Prints the version of the drowsy_server package.",
    ),
) -> None:
    """Show the main interface"""
    show_interface()


if __name__ == "__main__":
    app()
