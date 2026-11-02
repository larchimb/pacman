"""Throwaway test of BoardView: draw the walls of a real level."""

import time

from src.graphical.board_view import BoardView
from src.graphical.renderer import Renderer
from src.logical.game import Game
from src.logical.mazeloader import MazeLoader
from src.logical.parser import Parser

# Same window size as the real game.
renderer = Renderer(1440, 960, "Test board")
# Created once, before the loop: BoardView builds its wall images
# in __init__, and Game generates every maze when it is created.
board = BoardView(renderer)
game = Game(MazeLoader(Parser().check_file("config.json")))

running = True
while running:
    for event in renderer.poll_events():
        if event.kind == "quit" or event.key == "escape":
            running = False
        # Test only: next level, to check every maze size is centered.
        elif event.kind == "key_down" and event.key == "n":
            game.pass_level()

    renderer.clear()
    board.draw(renderer, game.level._maze)
    renderer.present()
    time.sleep(1 / 60)

renderer.close()
