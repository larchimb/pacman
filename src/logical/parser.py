import json
from .models import ParsingError
from typing import Any


class Parser():
    '''Check all datas in entry'''
    def __init__(self) -> None:
        '''Initialazing variables to return'''
        self.raw_data: str = ""
        self.data: dict[str, Any] = {}

    def check_file(self, path: str) -> None:
        '''To check if the file exist and is authorized'''
        try:
            with open(path) as f:
                text = f.read()
        except FileNotFoundError as e:
            raise Exception(f"[ERROR]: {e}")
        except OSError as e:
            raise Exception(f"[ERROR]: file '{path}' is locked")
        self.delete_comments(text)
        self.check_json_format()
        print(self.raw_data)

    def delete_comments(self, raw_text: str) -> None:
        '''Delete all comments in the file'''
        all_rows = raw_text.splitlines()
        for row in all_rows:
            for letter in row:
                if letter == "#":
                    row = row[:row.index(letter)]
                    break
            self.raw_data += row + "\n"

    def check_json_format(self) -> None:
        '''To check if it is the right format'''
        try:
            self.data: dict[str, Any] = json.loads(self.raw_data)
        except json.JSONDecodeError as e:
            raise ParsingError(f"{e}")


class Config():
    '''A class with all the parameters and the default value'''
    def __init__(self, data: dict[str, Any]) -> None:
        self.data = data
        self.highscores: dict[str, int] = {}
        self.get_highscores()


    def get_highscores(self) -> None:
        '''Obtain the highscores from the file'''
        path_to_highscores = self.data.get("highscore_filename")
        if not path_to_highscores:
            path_to_highscores = "highscores.json"
        try:
            with open(path_to_highscores) as f:
                self.highscores = json.load(f)
        except FileNotFoundError as e:
            raise Exception(f"[ERROR]: {e}")
        except OSError as e:
            raise Exception(f"[ERROR]: file '{path_to_highscores}' is locked")
