from codecs import ignore_errors
import json
from pathlib import Path
from subprocess import Popen, PIPE


PATH = 'C:\Steam\steamapps\common\wallpaper_engine'
CONFIG_FILE = 'config.json'
EXE32 = 'wallpaper32.exe'
EXE64 = 'wallpaper64.exe'
HIDE_WINDOW = 0x08000000


def get_config(path=PATH):
    path = str(path)
    full_path = Path(path, CONFIG_FILE)
    with open(full_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def get_profiles(wallpaper_engine_path, exe=EXE32):
    config = get_config(wallpaper_engine_path)
    user_key = list(config.keys())[1]
    return [Profile(p, wallpaper_engine_path, exe) for p in config[user_key]['general'].get('profiles', [])]


def cmd(command):
    return Popen(command, stdout=PIPE, stderr=PIPE, shell=True, creationflags=HIDE_WINDOW)


def set_profile(profile_name, wallpaper_engine_dir, exe):
    exe_path = Path(wallpaper_engine_dir, exe)
    args = f'"{exe_path}" -control openProfile -profile "{profile_name}"'
    cmd(args)


class WallpaperEngine(object):

    def __init__(self, wallpaper_engine_dir, exe=EXE32):
        self.wallpaper_engine_dir = wallpaper_engine_dir
        self.exe = exe
        self.config = get_config(self.wallpaper_engine_dir)
        self.profiles = get_profiles(
            self.wallpaper_engine_dir, self.exe)


class Profile(object):

    def __init__(self, data, wallpaper_engine_path, exe=EXE32):
        self.data = data
        self.wallpaper_engine_path = wallpaper_engine_path
        self.exe = exe
        for k, v in data.items():
            setattr(self, k, v)

    def set(self):
        set_profile(self.name, self.wallpaper_engine_path, self.exe)
