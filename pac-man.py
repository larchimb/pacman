import mazegenerator
from src.logical.parser import ParsingError
from src.logical.parser import Parser
import sys


def main() -> None:
    '''Entry point of the programm'''
    av = sys.argv
    if not len(av) == 2:
        raise Exception("[ERROR]: You must have 1 argument for this programm")
    parser = Parser(av[1])

if __name__ == "__main__":
    try:
        main()
    except(ParsingError, Exception, KeyboardInterrupt) as e:
        print(e)