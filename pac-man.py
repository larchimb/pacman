"""Entry point of the game: load the config and open the window."""


def main() -> None:
    '''Entry point of the programm'''
    from src.logical.parser import Parser, ParsingError
    from src.logical.mazeloader import MazeLoader
    from src.graphical.app import App
    import sys
    from src.paths import config_path

    path = config_path(sys.argv)
    try:
        raw = Parser.check_file(path)
    except ParsingError as e:
        print(f"{e}, the default config is used")
        raw = {}
    config = MazeLoader(raw)
    launch = App(2048, 1450, "Pac-Man", config)
    launch.run()


if __name__ == "__main__":
    try:
        main()
    except (Exception, KeyboardInterrupt) as e:
        print(e)
