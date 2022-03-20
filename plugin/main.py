from flox import Flox, ICON_APP_ERROR, FLOW_API, WOX_API

import wallpaper_engine as we
from wallpaper_engine import PATH, EXE32

class WallpaperEngineProfileSelector(Flox):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.config_path = self.settings.get('config_path', PATH)
        self.exe = self.settings.get('exe', EXE32)


    def query(self, query):
        try:
            profiles = we.get_profiles(self.config_path, self.exe)
            if len(profiles) == 0:
                self.add_item(
                    title='No profiles found',
                    subtitle='Please create a profile in Wallpaper Engine.',
                    icon=ICON_APP_ERROR
                )
            for profile in profiles:
                if query.lower() in profile.name.lower():
                    self.add_item(
                        title=profile.name,
                        subtitle='Set Wallpaper Engine to use this profile.',
                        icon=self.icon,
                        method=self.select_profile,
                        parameters=[profile.name]
                    )
        except FileNotFoundError:
            self.add_item(
                title='Wallpaper Engine not found',
                subtitle='Please provide the path to Wallpaper Engine in settings.',
                icon=ICON_APP_ERROR,
                method=self.open_setting_dialog
            )

    def context_menu(self, data):
        profile_name = data[0]
        self.add_item(
            title=f'Set the wallpaper profile to {profile_name}',
            subtitle='Sets Wallpaper Engine to use this profile.',
            icon=self.icon,
            method=self.select_profile,
            parameters=[profile_name]
        )

    def select_profile(self, profile_name):
        profiles = we.set_profile(profile_name, self.config_path, self.exe)

if __name__ == "__main__":
    WallpaperEngineProfileSelector()
