import json
import sys
from getpass import getuser
from pathlib import Path
from subprocess import PIPE, Popen
from typing import List, Optional

DEFAULT_DIR = r"C:\Steam\steamapps\common\wallpaper_engine"
CONFIG_FILE = "config.json"
EXE32 = "wallpaper32.exe"
EXE64 = "wallpaper64.exe"
NON_USER_KEYS = frozenset({"?installdirectory", "_installdirectory"})
CREATE_NO_WINDOW = 0x08000000


def read_config(directory: str) -> dict:
    with open(Path(directory, CONFIG_FILE), encoding="utf-8") as file:
        return json.load(file)


def current_user() -> Optional[str]:
    try:
        return getuser()
    except (ImportError, KeyError, OSError):
        return None


def user_profiles(user: object) -> List[str]:
    if not isinstance(user, dict):
        return []
    profiles = user.get("general", {}).get("profiles") or []
    return [profile["name"] for profile in profiles if "name" in profile]


def profile_names(config: dict) -> List[str]:
    users = {key: user_profiles(value) for key, value in config.items() if key not in NON_USER_KEYS}
    username = (current_user() or "").casefold()
    for key, profiles in users.items():
        if key.casefold() == username and profiles:
            return profiles
    return next((profiles for profiles in users.values() if profiles), [])


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
