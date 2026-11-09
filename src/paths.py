import os
import sys

if getattr(sys, "frozen", False):
    # Packaged game: bundled files in _internal/, saves next to the exe
    BUNDLE_DIR: str = getattr(sys, "_MEIPASS")
    USER_DIR: str = os.path.dirname(sys.executable)
else:
    # Local: the project root (this file is in src/, so go up once)
    BUNDLE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    USER_DIR = BUNDLE_DIR

CONFIG_NAME: str = "config.json"


def resource_path(relative: str) -> str:
    '''Path of a file shipped with the game (assets, default config)'''
    return os.path.join(BUNDLE_DIR, relative)


def user_path(relative: str) -> str:
    '''Path of a file written by the game (highscores)'''
    return os.path.join(USER_DIR, relative)


def config_path(av: list[str]) -> str:
    '''Config to use: the argument if given, else the one next to the
    game (editable by the player), else the one shipped in the package'''
    if len(av) > 1:
        return av[1]
    user_config = user_path(CONFIG_NAME)
    if os.path.isfile(user_config):
        return user_config
    return resource_path(CONFIG_NAME)
