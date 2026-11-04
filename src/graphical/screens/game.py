"""Game screen: the board and the HUD (empty for now)."""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.board_view import BoardView
from src.graphical.screens.screen import Screen
from src.logical.game import Game

if TYPE_CHECKING:
    from src.graphical.app import App

# Key of the keyboard -> action of Game.handle_action (Luc's strings).
ACTION_KEYS: dict[str, str] = {
    "up": "up", "w": "up",
    "down": "down", "s": "down",
    "left": "left", "a": "left",
    "right": "right", "d": "right",
    "c": "cheat",
    "1": "invincible", "2": "freeze", "3": "life",
    "4": "speed", "5": "level",
}
HUD_COLOR: int = 0xFFFFFF
HUD_Y: int = 28


class GameScreen(Screen):
    """Screen shown while playing."""

    def __init__(self, app: "App", game: Game) -> None:
        """Keep the game and build the board images once."""
        super().__init__(app)
        self.game = game
        self._board = BoardView(app.renderer)

    def handle_event(self, event: InputEvent) -> None:
        """Pause on Space, send every other known key to the game."""
        if event.kind != KEY_DOWN:
            return
        if event.key == "space":
            self._app.pause(self)
        elif event.key in ACTION_KEYS:
            self.game.handle_action(ACTION_KEYS[event.key])

    def update(self, dt: float) -> None:
        """Advance the game, then show the end screen if it is over."""
        self.game.update(dt)
        if self.game.result == "victory":
            self._app.end_game(True, self.game.score)
        elif self.game.result == "defeat":
            self._app.end_game(False, self.game.score)

    def draw(self, renderer: Renderer) -> None:
        """Draw the board, then the HUD above it."""
        game = self.game
        self._board.draw(renderer, game.level)
        renderer.string_put(40, HUD_Y, HUD_COLOR, f"Score: {game.score}")
        renderer.string_put(400, HUD_Y, HUD_COLOR, f"Lives: {game.lives}")
        renderer.string_put(
            700, HUD_Y, HUD_COLOR, f"Level: {game.current_level + 1}"
        )
        renderer.string_put(
            1000, HUD_Y, HUD_COLOR, f"Time: {max(0, int(game.level_timer))}"
        )
