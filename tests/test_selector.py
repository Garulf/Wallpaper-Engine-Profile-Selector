import selector
import wallpaper_engine as we
from conftest import user


def titles(results):
    return [result.title for result in results]


def test_query_lists_matching_profiles_in_config_order(settings, write_config):
    write_config({"?installdirectory": "C:/WE", "alice": user("Desk", "Gaming", "Desk Night")})
    assert titles(selector.query("")) == ["Desk", "Gaming", "Desk Night"]
    assert titles(selector.query("DESK")) == ["Desk", "Desk Night"]


def test_profile_result_selects_profile(settings, write_config):
    write_config({"alice": user("Gaming")})
    action = selector.query("gam")[0].to_json()["JsonRPCAction"]
    assert action["Method"] == "select_profile"
    assert action["Parameters"] == ["Gaming"]


def test_missing_wallpaper_engine_opens_settings(settings):
    settings["config_path"] = settings["config_path"] + "/missing"
    (result,) = selector.query("")
    assert result.title == "Wallpaper Engine not found"
    assert result.to_json()["JsonRPCAction"]["Method"] == "Flow.Launcher.OpenSettingDialog"


def test_no_profiles(settings, write_config):
    write_config({"alice": {"general": {"profiles": []}}})
    assert titles(selector.query("")) == ["No profiles found"]


def test_select_profile_uses_settings(settings, launched, tmp_path):
    selector.select_profile("Gaming")
    ((args, _),) = launched
    assert str(tmp_path / we.EXE64) in str(args)


def test_defaults_when_settings_are_empty():
    assert selector.wallpaper_engine_settings() == (we.DEFAULT_DIR, we.EXE32)


def test_context_menu_selects_profile():
    (result,) = selector.context_menu(["Gaming"])
    assert result.title == "Set the wallpaper profile to Gaming"
    assert result.to_json()["JsonRPCAction"]["Parameters"] == ["Gaming"]
