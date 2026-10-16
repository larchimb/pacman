from typing import Any
from parser import Parser

class MazeLoader():
    '''A class with all the parameters and the default value'''
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.highscores: dict[str, int] = {}
        self.get_highscores()
        print(self.highscores)

    def get_highscores(self) -> dict[str, int]:
        '''Obtain the highscores from the file'''
        path_to_highscores = self.data.get("highscore_filename")
        if not path_to_highscores:
            path_to_highscores = "highscores.json"
        datas = Parser.check_file(path_to_highscores)
        for key, value in datas.items():
            if 
        return