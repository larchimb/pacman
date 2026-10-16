import json
from typing import Any

class ParsingError(Exception):
    '''Contain all errors due to the parsing'''
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"[PARSING ERROR]: {super().__str__()}"


class Parser():
    '''Check the json format without the comments'''
    @staticmethod
    def check_file(path: str) -> dict[str, Any]:
        '''Read the file, remove comments and check the JSON format'''
        try:
            with open(path, encoding="utf-8") as f:
                text = f.read()
        except FileNotFoundError as e:
            raise ParsingError(f"file '{path}' not found") from e
        except PermissionError as e:
            raise ParsingError(f"no permission to read '{path}'") from e
        except UnicodeDecodeError as e:
            raise ParsingError(f"file '{path}' is not valid UTF-8") from e
        except OSError as e:
            raise ParsingError(f"cannot read '{path}': {e}") from e
        raw_data = Parser.delete_comments(text)
        return Parser.check_json_format(raw_data)

    @staticmethod
    def delete_comments(raw_text: str) -> str:
        '''Delete all comments in the file'''
        all_rows = raw_text.splitlines()
        raw_data = ""
        for row in all_rows:
            for letter in row:
                if letter == "#":
                    row = row[:row.index(letter)]
                    break
            raw_data += row + "\n"
        return raw_data

    @staticmethod
    def check_json_format(raw_data: str) -> dict[str, Any]:
        '''To check if it is a valid JSON with a dict'''
        try:
            data = json.loads(raw_data)
        except json.JSONDecodeError as e:
            raise ParsingError(f"invalid JSON: {e}") from e
        if not isinstance(data, dict):
            raise ParsingError("format must be a dict object")
        return data
