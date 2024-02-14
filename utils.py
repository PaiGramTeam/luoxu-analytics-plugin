from typing import Optional
import subprocess
from sys import executable
from importlib.util import find_spec


def pip_install(
    package: str, version: Optional[str] = "", alias: Optional[str] = ""
) -> bool:
    """Auto install extra pypi packages"""
    if not alias:
        # when import name is not provided, use package name
        alias = package
    if find_spec(alias) is None:
        subprocess.call([executable, "-m", "pip", "install", f"{package}{version}"])
        if find_spec(package) is None:
            return False
    return True
