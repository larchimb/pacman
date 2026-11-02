"""Throwaway test of the BoardView with the FakeGame."""

from src.graphical.board_view import BoardView
from src.graphical.fake_game import FakeGame
from src.graphical.renderer import Renderer

renderer = Renderer(1440, 960, "Test board")
board = BoardView(renderer)
game = FakeGame()

running = True
while running:
    for event in renderer.poll_events():
        if event.kind == "quit" or event.key == "escape":
            running = False
    renderer.clear()
    board.draw(renderer, game.level.maze)
    renderer.present()

renderer.close()
