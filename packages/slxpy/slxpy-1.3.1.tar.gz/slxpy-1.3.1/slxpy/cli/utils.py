import sys
from pathlib import Path
from typing import Optional

import slxpy.common.constants as C


DEBUG = False
def set_debug(debug: bool):
    global DEBUG
    DEBUG = debug


def is_debug():
    return DEBUG


def ensure_slxpy_project(workdir: Path):
    # Safe check except init subcommand
    if not (workdir / C.model_config_name).exists() or not (workdir / C.env_config_name).exists():
        raise Exception("Not a slxpy project directory.")


def get_plat_name():
    import distutils.util
    return distutils.util.get_platform()


def get_plat_specifier(version: Optional[str] = None) -> str:
    # Ported from distutils/command/build.py
    if version is None:
        version = f"{sys.version_info.major}.{sys.version_info.minor}"
    plat_name = get_plat_name()
    return f".{plat_name}-{version}"
