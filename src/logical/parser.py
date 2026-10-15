class ParsingError(Exception):
    "Contain all errors due to the parsing"
    def __init__(self, message: str) -> None:
        super().__init__(message)

    def __str__(self) -> str:
        return f"[PARSING ERROR]: {super().__str__()}"


class Parser():
    '''Check all datas in entry'''
    def __init__(self, path: str) -> None:
        with 