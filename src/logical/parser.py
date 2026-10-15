import json


class ParsingError(Exception):
    "Contain all errors due to the parsing"
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"[PARSING ERROR]: {super().__str__()}"


class Parser():
    '''Check all datas in entry'''
    def __init__(self) -> None:
        '''Initialazing variables to return'''
        self.raw_data: str = ""
        self.data =

    def check_file(self, path: str) -> None:
        '''To check if the file exist and is authorized'''
        try:
            with open(path) as f:
                text = f.read()
        except FileNotFoundError as e:
            raise e
        except OSError as e:
            raise Exception(f"[ERROR]: Unable to read file '{path}'")
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


