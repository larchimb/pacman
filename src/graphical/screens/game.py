"""Game screen: the board and the HUD (empty for now)."""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen
from src.logical.game import Game

if TYPE_CHECKING:
    from src.graphical.app import App

# Keys that move Pac-Man: arrows and WASD give the same direction.
DIRECTION_KEYS: dict[str, str] = {
    "up": "up", "w": "up",
    "down": "down", "s": "down",
    "left": "left", "a": "left",
    "right": "right", "d": "right",
}


class GameScreen(Screen):
    """Screen shown while playing."""

    def __init__(self, app: "App", game: Game) -> None:
        """Start with no direction asked yet."""
        super().__init__(app)
        # Last direction asked by the player (sent to the game later).
        self._direction: str = "none"
        self.game = game

    def handle_event(self, event: InputEvent) -> None:
        """Pause on Space, remember the last direction key."""
        if event.kind != KEY_DOWN:
            return
        action = ""
        if event.key == "space":
            self._app.pause(self)
            action = "pause"
        elif event.key in DIRECTION_KEYS:
            action = DIRECTION_KEYS[event.key]
        # Temporary test keys until the real Game says when it ends.
        elif event.key == "c":
            action = "cheat"
        elif event.key == "1":
            action = "invincible"
        elif event.key == "2":
            action = "freeze"
        elif event.key == "3":
            action = "life"
        elif event.key == "4":
            action = "speed"
        elif event.key == "5":
            action = "level"
        elif event.key == "g":
            self._app.end_game(False, 0)
        elif event.key == "v":
            self._app.end_game(True, 0)
        self.game.handle_action(action)

    def update(self, dt: float) -> None:
        '''The main loop for animation'''
        while not self.game.result:
            ...


    def draw(self, renderer: Renderer) -> None:
        """Draw the game (only text for now)."""
        renderer.string_put(20, 20, 0xFFFF00, "GAME")
        renderer.string_put(
            20, 50, 0xFFFFFF, f"Direction: {self._direction}"
        )
        renderer.string_put(20, 80, 0x888888, "Space: pause")
        renderer.string_put(20, 110, 0x888888, "G: game over")
        renderer.string_put(20, 140, 0x888888, "V: victory")
