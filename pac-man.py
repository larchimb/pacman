from src.logical.parser import Parser, ParsingError
from src.logical.mazeloader import MazeLoader
from src.logical.game import Game
import sys


def main() -> None:
    '''Entry point of the programm'''
    av = sys.argv
    if not len(av) == 2:
        raise Exception("[ERROR]: You must have 1 argument for this programm")
    parser = Parser()
    config = MazeLoader(parser.check_file(av[1]))
    game = Game(config)

if __name__ == "__main__":
    # try:
        main()
    # except(ParsingError, Exception, KeyboardInterrupt) as e:
        # print(e)