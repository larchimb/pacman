from typing import Any
from .parser import Parser, ParsingError
from pydantic import BaseModel


class Level(BaseModel):
    '''A model class for levels'''


class MazeLoader():
    '''A class with all the parameters and the default value'''
    def __init__(self,
                 data: dict[str, Any]) -> None:
        self.raw_data = data
        self.datas = {
        "highscore": ".highscores.json",
        "levels": [
        [10, 10],
        [11, 11],
        [12, 12],
        [13, 13],
        [14, 14],
        [15, 15],
        [16, 16],
        [17, 17],
        [18, 18],
        [19, 19]
        ],
        "lives": 3,
        "pacgum": 50,
        "points_per_pacgum": 10,
        "points_per_superpacgum": 50,
        "points_per_ghost": 200,
        "seed": 42,
        "level_max_time": 90
        }
        self.width_min = 9
        self.width_max = 20
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
            if not isinstance(value, int) or isinstance(value, bool):
                raise ParsingError("the score must be a int")
        return datas

    def get_levels(self) -> list[list[int]]:
        '''To set up the levels'''
        levels = self.raw_data.get("levels")
        if not levels:
            return self.datas["levels"]
        for level in range(0, 9):
            width = levels[level][0]
            if (not isinstance(width, int)
                or isinstance(width, bool)
                or not (self.width_min <
                        width < self.width_max)):
                print(f"[VALUE ERROR]: level {level + 1}, '{width}' isn't good,"
                      f" the default's width value is applied")
                width = self.datas["levels"][level][0]
            height = levels[level][1]
            if (not isinstance(height, int)
                or isinstance(height, bool)
                or not (self.height_min <
                        height < self.height_max)):
                print(f"[VALUE ERROR]: level {level + 1}, '{height}' "
                      f"isn't good, the default's height value is applied")
                height = self.datas["levels"][level][1]
            levels[level][0] = width
            levels[level][1] = height
        return levels

    def get_values(self) -> None:
        '''To check and complete all settings'''
        for setting in self.datas.keys():
            if setting == "highscore":
                self.datas[setting] = self.get_highscores()
            elif setting == "levels":
                self.datas[setting] = self.get_levels()
            else:
                value = self.raw_data.get(setting)
                if not value:
                    print(f"[VALUE ERROR]: no value for {setting}, "
                          "the default one is choosen")
                else:
                    self.datas[setting] = value
