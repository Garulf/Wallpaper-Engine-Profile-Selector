import json

import pytest

import selector
import wallpaper_engine


def user(*profiles):
    return {"general": {"profiles": [{"name": name, "monitors": {}} for name in profiles]}}


@pytest.fixture
def write_config(tmp_path):
    def write(config):
        (tmp_path / wallpaper_engine.CONFIG_FILE).write_text(json.dumps(config), encoding="utf-8")
        return tmp_path

    return write


@pytest.fixture
def settings(tmp_path):
    launcher = selector.plugin.launcher
    launcher._settings = {"config_path": str(tmp_path), "exe": wallpaper_engine.EXE64}
    yield launcher._settings
    launcher._settings = {}


class FakePopen:
    calls = []

    def __init__(self, args, **kwargs):
        FakePopen.calls.append((args, kwargs))


@pytest.fixture
def launched(monkeypatch):
    FakePopen.calls = []
    monkeypatch.setattr(wallpaper_engine, "Popen", FakePopen)
    return FakePopen.calls
