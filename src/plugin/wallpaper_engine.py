import json
import sys
from pathlib import Path
from subprocess import PIPE, Popen
from typing import List

DEFAULT_DIR = r"C:\Steam\steamapps\common\wallpaper_engine"
CONFIG_FILE = "config.json"
EXE32 = "wallpaper32.exe"
EXE64 = "wallpaper64.exe"
NON_USER_KEYS = frozenset({"?installdirectory", "_installdirectory"})
CREATE_NO_WINDOW = 0x08000000


def read_config(directory: str) -> dict:
    with open(Path(directory, CONFIG_FILE), encoding="utf-8") as file:
        return json.load(file)


def profile_names(config: dict) -> List[str]:
    for key in config:
        if key in NON_USER_KEYS:
            continue
        user = config[key]
    return [profile["name"] for profile in user["general"].get("profiles", [])]


def profile_command(name: str, directory: str, exe: str) -> str:
    return f'"{Path(directory, exe)}" -control openProfile -profile "{name}"'


def open_profile(name: str, directory: str, exe: str) -> None:
    Popen(
        profile_command(name, directory, exe),
        stdout=PIPE,
        stderr=PIPE,
        shell=True,
        creationflags=CREATE_NO_WINDOW if sys.platform == "win32" else 0,
    )
