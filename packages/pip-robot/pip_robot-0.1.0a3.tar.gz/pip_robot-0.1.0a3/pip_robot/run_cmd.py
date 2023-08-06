"""Run a command via subprocess.Popen."""
import re
import subprocess as sp
from shlex import split
import logzero
from logzero import logger

from pip_robot import loglevel

name_mapping = {"pil": "pillow"}


def run_cmd(
    cmd: str,
    debug: bool = False,
) -> str:
    """Run a command.

    Args:
        cmd: str
        debug: turn on debug if True (default: False)
    Returns:
        module_name: name of the missing package

    cmd = "python func.py"
    """
    old_loglevel = logger.level
    if debug:
        logzero.loglevel(loglevel(10))
    try:
        with sp.Popen(
            split(cmd),
            stdout=-1,
            stderr=-1,
            text=True,
            shell=True,
        ) as proc:
            out, err = proc.communicate()
    except Exception as exc:
        logger.exception(exc)
        raise

    if out:
        logger.debug("Out: %s", out)
    if err:
        logger.debug("err: %s", err)

    # if "ModuleNotFoundError" in err:
    module_name = ""
    if "No module named" in err:
        try:
            _ = err.splitlines()[-1]
            _ = re.findall(r"(?<=')[\w_-]+", _)
            if _:
                module_name = _[0]
        except Exception as exc:
            logger.exception(exc)
            raise

    # restore loglevel
    if debug:
        logzero.loglevel(old_loglevel)

    if module_name in name_mapping:
        module_name = name_mapping.get(module_name)

    return module_name
