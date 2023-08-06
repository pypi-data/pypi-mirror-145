"""Prep __main__ entry."""
# pylint: disable=invalid-name
from typing import List, Optional

import logzero
from logzero import logger
import typer
from icecream import ic, install as ic_install

from pip_robot import __version__, pip_robot, loglevel

logzero.loglevel(loglevel())

ic_install()
ic.configureOutput(
    includeContext=True,
    # outputFunction=logger.info,
    outputFunction=logger.debug,
)
ic.enable()

app = typer.Typer(
    name="ezbee",
    add_completion=False,
    help="en-zh-bee aligner",
)


ic_install()
ic.configureOutput(
    includeContext=True,
    # outputFunction=logger.info,
    outputFunction=logger.debug,
)
ic.enable()

app = typer.Typer(
    name="pip-robot",
    add_completion=False,
    help="pip install robot",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(
            f"{app.info.name} v.{__version__}"
        )
        raise typer.Exit()


@app.command()
def main(
    command: List[str] = typer.Argument(
        ...,
        metavar="command [args or options]...",
        help="""a command to check against missing pyi packages, typically python foo.py or "python -m bar" (note the quotes) """,
    ),
    debug: bool = typer.Option(
        False,
        "--debug",
        "-d",
        is_flag=True,
        help="Turn on debug mode. Note that debug can also be turned by set LOGLEVEL=debug or export LOGLEVEL=debug.",
    ),
    version: Optional[bool] = typer.Option(  # pylint: disable=(unused-argument
        None,
        "--version",
        "-v",
        "-V",
        help="Show version info and exit.",
        callback=_version_callback,
        is_eager=True,
    ),
):
    """Install missing pypi packages, automatically with best-effort.

    e.g.

    pip-robot python foo.py

    or pythom -m pip_robot python foo.py

    or pip-robot "python -m bar"  # (must enclosed in quotes
    if options (- or/and --) are present in the command to test.)

    """
    if debug:
        logger.info("debug is on")
        # logzero.loglevel(loglevel(10, force=True))
        # logzero.loglevel(loglevel(10))
        # logzero.loglevel(loglevel(20, force=True))

    logger.debug("debug")

    typer.echo(f"Your command: {' '.join(command)}")
    logger.info("Nothing yet... we are working on it.")
    # raise NotImplementedError("Coming soon...")


if __name__ == "__main__":
    # set LOGLEVEL=10 or debug or DEBUG to turn on debug
    logger.debug(" debug on (main)")
    app()
    logger.debug("wont show debug on (main) 1")
