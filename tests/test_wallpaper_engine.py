from subprocess import PIPE

import pytest

import wallpaper_engine as we
from conftest import user


def test_read_config_missing_directory(tmp_path):
    with pytest.raises(FileNotFoundError):
        we.read_config(str(tmp_path / "missing"))


def test_profile_names_skip_install_directory(write_config):
    directory = write_config({"?installdirectory": "C:/WE", "alice": user("Desk", "Gaming")})
    assert we.profile_names(we.read_config(str(directory))) == ["Desk", "Gaming"]


def test_profile_names_without_profiles():
    assert we.profile_names({"alice": {"general": {}}}) == []


def test_open_profile_launches_wallpaper_engine(launched, tmp_path):
    we.open_profile("Desk Night", str(tmp_path), we.EXE64)
    assert launched == [
        (
            f'"{tmp_path / we.EXE64}" -control openProfile -profile "Desk Night"',
            {"stdout": PIPE, "stderr": PIPE, "shell": True, "creationflags": 0},
        )
    ]


def test_open_profile_hides_console_on_windows(launched, monkeypatch, tmp_path):
    monkeypatch.setattr(we.sys, "platform", "win32")
    we.open_profile("Gaming", str(tmp_path), we.EXE32)
    ((_, kwargs),) = launched
    assert kwargs["creationflags"] == we.CREATE_NO_WINDOW == 0x08000000
