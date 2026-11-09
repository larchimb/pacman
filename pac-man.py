def main() -> None:
    '''Entry point of the programm'''
    from src.logical.parser import Parser, ParsingError
    from src.logical.mazeloader import MazeLoader
    from src.graphical.app import App
    import sys

    av = sys.argv
    # if not len(av) == 2:
    #     raise Exception("[ERROR]: You must have 1 argument for this programm")
    try:
        raw = Parser.check_file(av[1])
    except Exception as e:
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
