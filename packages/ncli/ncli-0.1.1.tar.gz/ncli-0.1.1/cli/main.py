from typing import Optional

import typer

from cli.commands import find
from cli.utils import get_version
from cli.settings import load_settings

settings = load_settings()

app = typer.Typer(add_completion=False)
app.add_typer(find.app, name="find")


def version_callback(value: bool):
    if value:
        typer.echo(f"ncli version: {get_version()}")
        raise typer.Exit()


@app.callback()
def version(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        callback=version_callback,
        is_eager=True,
        help="Returns CLI version",
    )
):
    pass
