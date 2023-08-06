"""Prep __main__ entry."""
from typing import List, Optional

from install import install
import logzero
from logzero import logger
import typer

from pip_robot import __version__, loglevel
from pip_robot.run_cmd import run_cmd

logzero.loglevel(loglevel())

app = typer.Typer(
    name="ezbee",
    add_completion=False,
    help="en-zh-bee aligner",
)

app = typer.Typer(
    name="pip-robot",
    add_completion=False,
    help="pip install robot",
)


def _version_callback(value: bool) -> None:
    if value:
        typer.echo(f"{app.info.name} v.{__version__}")
        raise typer.Exit()


@app.command()
def main(
    command: List[str] = typer.Argument(
        ...,
        metavar="command [args or options]...",
        help="""a command to check against missing pyi packages, typically python foo.py or "python -m bar" (note the quotes) """,
    ),
    max_try: int = typer.Option(6, "--max-try", "-m", help="Try max_try times."),
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
        # logzero.loglevel(loglevel(20, force=True))
        logzero.loglevel(loglevel(10))

    logger.debug("debug")

    cmd = " ".join(command)
    typer.echo(f"Your command: {cmd}")
    logger.debug("Nothing much yet... we are working on it.")
    # raise NotImplementedError("Coming soon...")

    missing_list = []
    for _ in range(max_try):
        try:
            missing = run_cmd(cmd)
        except Exception as exc:
            logger.exception(exc)
            raise typer.Exit(1)

        if missing:
            try:
                logger.info("Installing: %s", missing)
                install(missing)
                logger.debug("Done isnstalling: %s", missing)
                missing_list.append(missing)
            except Exception as exc:
                logger.exception(exc)
                raise typer.Exit(1)

        # nothing missing break
        if not missing:
            break

    logger.info("Installed: %s", missing_list)


if __name__ == "__main__":
    # set LOGLEVEL=10 or debug or DEBUG to turn on debug
    logger.debug(" debug on (main)")
    app()
