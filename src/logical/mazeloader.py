from typing import Any
from .parser import Parser, ParsingError


class MazeLoader():
    '''A class with all the parameters and the default value'''
    def __init__(self,
                 data: dict[str, Any]) -> None:
        self.raw_data = data
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
         "lives": 3,
         "pacgum": 50,
         "points_per_pacgum": 10,
         "points_per_superpacgum": 50,
         "points_per_ghost": 200,
         "seed": 42,
         "level_max_time": 90
        }
        self.width_min = 13
        self.width_max = 24
        self.height_min = 9
        self.height_max = 20
        self.get_values()

    def get_highscores(self) -> dict[str, int]:
        '''Obtain the highscores from the file'''
        try:
            path = self.raw_data.get("highscore_filename")
            if not path:
                raise ParsingError("no file for highscore")
            datas = Parser.check_file(path)
            return self.check_highscores(datas)
        except ParsingError as e:
            print(f"{e}, the default one is choosen")
        path = self.datas["highscore"]
        try:
            datas = Parser.check_file(path)
            return self.check_highscores(datas)
        except ParsingError as e:
            print(f"{e}, a new highscore file is created")
        with open(path, "w", encoding="utf-8") as f:
            f.write("{}")
        return {}

    @staticmethod
    def check_highscores(datas: dict[str, Any]) -> dict[str, int]:
        '''Check names and scores of the highscores'''
        for key, value in datas.items():
            if len(key) > 10:
                raise ParsingError(f"{key} is too long, max 10 characters")
            if (not isinstance(value, int)
               or isinstance(value, bool)
               or value < 0):
                raise ParsingError("the score must be a positiv int")
        return datas

    @staticmethod
    def is_valid_int(value: Any, minimum: int, maximum: int) -> bool:
        '''Check if value is an int strictly between minimum and maximum'''
        if (isinstance(value, int)
                and not isinstance(value, bool)
                and minimum < value < maximum):
            return True
        return False

    def get_levels(self) -> list[list[int]]:
        '''To set up the levels'''
        levels = self.raw_data.get("levels")
        default_levels: list[list[int]] = self.datas["levels"]
        if not levels:
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
            if not self.is_valid_int(width, self.width_min, self.width_max):
                print(f"[VALUE ERROR]: level {i + 1}, '{width}' isn't good "
                      f"({self.width_min}< value <{self.width_max}), "
                      "the default's width value is applied")
                width = default_width
            if not self.is_valid_int(height, self.height_min, self.height_max):
                print(f"[VALUE ERROR]: level {i + 1}, '{height}' isn't good "
                      f"({self.height_min}< value <{self.height_max}), "
                      "the default's height value is applied")
                height = default_height
            checked_levels.append([width, height])
        return checked_levels

    def get_values(self) -> None:
        '''To check and complete all settings'''
        for setting in self.datas.keys():
            if setting == "highscore":
                self.datas[setting] = self.get_highscores()
            elif setting == "levels":
                self.datas[setting] = self.get_levels()
            else:
                value = self.raw_data.get(setting)
                if not self.is_valid_int(value, 0, 10000):
                    print("[VALUE ERROR]: no value / negativ value for "
                          f"{setting}, the default one is choosen")
                else:
                    self.datas[setting] = value
