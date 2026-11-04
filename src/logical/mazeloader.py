from typing import Any
from .parser import Parser, ParsingError
import json


WIDTH_MIN = 14
WIDTH_MAX = 37
HEIGHT_MIN = 10
HEIGHT_MAX = 25
LIFE_MIN = 3
LIFE_MAX = 99
TIME_MIN = 60
TIME_MAX = 800
PACGUM_MIN = 20
PACGUM_MAX = 10000
INT_MIN_GAME = 10
INT_MAX_GAME = 10000


class MazeLoader():
    '''A class with all the parameters and the default value'''
    def __init__(self,
                 data: dict[str, Any]) -> None:
        self.raw_data = data
        self.path_to_highscore: str = ".highscores.json"
        self.datas: dict[str, Any] = {
         "highscore": ".highscores.json",
         "levels": [
            [14, 10],
            [15, 11],
            [16, 12],
            [17, 13],
            [18, 14],
            [19, 15],
            [20, 16],
            [21, 17],
            [22, 18],
            [23, 19]
         ],
         "lives": LIFE_MIN,
         "pacgum": PACGUM_MAX,
         "points_per_pacgum": 10,
         "points_per_supergum": 50,
         "points_per_ghost": 200,
         "seed": 41,
         "level_max_time": 90
        }
        self.get_values()

    def get_highscores(self) -> list[dict[str, int]]:
        '''Obtain the highscores from the file'''
        try:
            path = self.raw_data.get("highscore_filename")
            if not path:
                raise ParsingError("no file for highscore")
            datas = Parser.check_file(path)
            self.path_to_highscore = path
            return self.check_highscores(datas)
        except ParsingError as e:
            print(f"{e}, the default one is choosen")
        path = self.datas["highscore"]
        try:
            datas = Parser.check_file(path)
            return self.check_highscores(datas)
        except ParsingError as e:
            print(f"{e}, a new highscore file is created")
        return []

    def save_score(self, name: str, score: int) -> bool:
        '''Add the score to the highscores and save the top 10'''
        name = name.strip()
        if not MazeLoader.is_valid_entry(name, score):
            return False
        highscores = self.datas["highscore"]
        highscores.append({"name": name, "score": score})
        self.datas["highscore"] = MazeLoader.top_ten(highscores)
        path = self.path_to_highscore
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"highscores": self.datas["highscore"]},
                          f, indent=2)
        except OSError as e:
            print(f"[SAVE ERROR]: cannot write '{path}': {e}")
            return False
        return True

    @staticmethod
    def is_valid_entry(name: Any, score: Any) -> bool:
        '''Check the name and the score of one highscore'''
        if not isinstance(name, str) or not name:
            print(f"[VALUE ERROR]: highscore '{name}' ignored, "
                  "the name must be a non-empty string")
        elif len(name) > 10:
            print(f"[VALUE ERROR]: highscore '{name}' ignored, "
                  "name too long (max 10 characters)")
        elif not name.replace(" ", "").isalnum():
            print(f"[VALUE ERROR]: highscore '{name}' ignored, "
                  "name must be alphanumeric")
        elif (not isinstance(score, int)
                or isinstance(score, bool)
                or score < 0):
            print(f"[VALUE ERROR]: highscore '{name}' ignored, "
                  "the score must be a positive int")
        else:
            return True
        return False

    @staticmethod
    def top_ten(entries: list[dict[str, Any]]) -> list[dict[str, Any]]:
        '''Sort the highscores by score and keep the 10 best'''
        return sorted(entries,
                      key=lambda entry: entry["score"], reverse=True)[:10]

    @staticmethod
    def check_highscores(datas: dict[str, Any]) -> list[dict[str, Any]]:
        '''Keep only the valid highscores, sorted, top 10'''
        entries = datas.get("highscores")
        if not isinstance(entries, list):
            print("[VALUE ERROR]: 'highscores' must be a list, "
                  "starting with an empty highscore list")
            return []
        valid: list[dict[str, Any]] = []
        for entry in entries:
            if not isinstance(entry, dict):
                print(f"[VALUE ERROR]: highscore '{entry}' ignored, "
                      "it must be {\"name\": ..., \"score\": ...}")
            elif MazeLoader.is_valid_entry(entry.get("name"),
                                           entry.get("score")):
                valid.append({"name": entry["name"],
                              "score": entry["score"]})
        return MazeLoader.top_ten(valid)

    @staticmethod
    def is_valid_int(value: Any, minimum: int, maximum: int) -> bool:
        '''Check if value is an int strictly between minimum and maximum'''
        if (isinstance(value, int)
                and not isinstance(value, bool)
                and minimum <= value <= maximum):
            return True
        return False

    def get_levels(self) -> list[list[int]]:
        '''To set up the levels'''
        levels = self.raw_data.get("levels")
        default_levels: list[list[int]] = self.datas["levels"]
        if not isinstance(levels, list) or not levels:
            print(
                "[VALUE ERROR]: no valid levels, the default ones are applied"
                )
            return default_levels
        checked_levels = []
        for i, (default_width, default_height) in enumerate(default_levels):
            if i >= len(levels):
                print(f"[VALUE ERROR]: level {i + 1} is missing, "
                      "the default one is applied")
                checked_levels.append([default_width, default_height])
                continue
            level = levels[i]
            if not isinstance(level, list) or not level:
                print(f"[VALUE ERROR]: level {i + 1}, '{level}' must be "
                      "[width, height], the default one is applied")
                checked_levels.append([default_width, default_height])
                continue
            width = level[0]
            if len(level) >= 2:
                height = level[1]
            else:
                print(f"[VALUE ERROR]: level {i + 1}, no height, "
                      "the default's height value is applied")
                height = default_height
            if not self.is_valid_int(width, WIDTH_MIN, WIDTH_MAX):
                print(f"[VALUE ERROR]: level {i + 1}, '{width}' isn't good "
                      f"({WIDTH_MIN} <= value <= {WIDTH_MAX}), "
                      "the default's width value is applied")
                width = default_width
            if not self.is_valid_int(height, HEIGHT_MIN, HEIGHT_MAX):
                print(f"[VALUE ERROR]: level {i + 1}, '{height}' isn't good "
                      f"({HEIGHT_MIN} <= value <= {HEIGHT_MAX}), "
                      "the default's height value is applied")
                height = default_height
            checked_levels.append([width, height])
        return checked_levels

    def get_lives(self, setting: str) -> None:
        '''To check lives number'''
        value = self.raw_data.get(setting)
        if not self.is_valid_int(value, LIFE_MIN, LIFE_MAX):
            print(f"[VALUE ERROR]: '{setting}' isn't good "
                  f"3 <= {setting} <= 99, the default one is applied")
        else:
            self.datas[setting] = value

    def get_max_time(self, setting: str) -> None:
        '''To check max time per level'''
        value = self.raw_data.get(setting)
        if not self.is_valid_int(value, TIME_MIN, TIME_MAX):
            print(f"[VALUE ERROR]: '{setting}' isn't good "
                  f"60 <= {setting} <= 600, the default one is applied")
        else:
            self.datas[setting] = value

    def get_pacgum(self, setting: str) -> None:
        '''To check pacgum per level'''
        value = self.raw_data.get(setting)
        if not self.is_valid_int(value, PACGUM_MIN, PACGUM_MAX):
            print(f"[VALUE ERROR]: '{setting}' isn't good "
                  f"10 <= {setting} , the default one is applied")
        else:
            self.datas[setting] = value

    def get_values(self) -> None:
        '''To check and complete all settings'''
        for setting in self.datas.keys():
            if setting == "highscore":
                self.datas[setting] = self.get_highscores()
            elif setting == "lives":
                self.get_lives(setting)
            elif setting == "level_max_time":
                self.get_max_time(setting)
            elif setting == "pacgum":
                self.get_pacgum(setting)
            elif setting == "levels":
                self.datas[setting] = self.get_levels()
            else:
                value = self.raw_data.get(setting)
                if not self.is_valid_int(value, INT_MIN_GAME, INT_MAX_GAME):
                    print("[VALUE ERROR]: no value / negativ value for "
                          f"{setting}, the default one is choosen")
                else:
                    self.datas[setting] = value
