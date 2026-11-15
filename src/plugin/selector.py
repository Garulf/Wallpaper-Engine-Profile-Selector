from pathlib import Path
from typing import List, Optional, Tuple

from pyflowlauncher import FlowLauncherV2, Plugin, Result, api

import wallpaper_engine as we

ICON = str(Path(__file__).resolve().parent.parent / "icon.png")

plugin = Plugin(launcher=FlowLauncherV2())


def wallpaper_engine_settings() -> Tuple[str, str]:
    settings = plugin.settings or {}
    return settings.get("config_path") or we.DEFAULT_DIR, settings.get("exe") or we.EXE32


def error_result(title: str, subtitle: str) -> Result:
    return Result(title=title, subtitle=subtitle, icon=plugin.launcher.icons.app_error)


@plugin.on_method
def select_profile(profile_name: str) -> None:
    directory, exe = wallpaper_engine_settings()
    we.open_profile(profile_name, directory, exe)


@plugin.on_method
def query(query: str) -> List[Result]:
    directory, _ = wallpaper_engine_settings()
    try:
        names = we.profile_names(we.read_config(directory))
    except FileNotFoundError:
        return [
            error_result(
                "Wallpaper Engine not found",
                "Please provide the path to Wallpaper Engine in settings.",
            ).add_action(api.open_setting_dialog())
        ]
    if not names:
        return [error_result("No profiles found", "Please create a profile in Wallpaper Engine.")]
    search = query.lower()
    return [
        Result(
            title=name,
            subtitle="Set Wallpaper Engine to use this profile.",
            icon=ICON,
            context_data=[name],
        ).add_action(select_profile, [name])
        for name in names
        if search in name.lower()
    ]


@plugin.on_method
def context_menu(data: Optional[list]) -> List[Result]:
    if not data:
        return []
    profile_name = data[0]
    return [
        Result(
            title=f"Set the wallpaper profile to {profile_name}",
            subtitle="Sets Wallpaper Engine to use this profile.",
            icon=ICON,
        ).add_action(select_profile, [profile_name])
    ]
