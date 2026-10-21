"""Game screen: the board and the HUD (empty for now)."""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

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

    def __init__(self, app: "App") -> None:
        """Start with no direction asked yet."""
        super().__init__(app)
        # Last direction asked by the player (sent to the game later).
        self._direction: str = "none"

    def handle_event(self, event: InputEvent) -> None:
        """Pause on Space, remember the last direction key."""
        if event.kind != KEY_DOWN:
            return
        if event.key == "space":
            self._app.pause(self)
        elif event.key in DIRECTION_KEYS:
            self._direction = DIRECTION_KEYS[event.key]
        # Temporary test keys until the real Game says when it ends.
        elif event.key == "g":
            self._app.end_game(False, 0)
        elif event.key == "v":
            self._app.end_game(True, 0)

    def draw(self, renderer: Renderer) -> None:
        """Draw the game (only text for now)."""
        renderer.string_put(20, 20, 0xFFFF00, "GAME")
        renderer.string_put(
            20, 50, 0xFFFFFF, f"Direction: {self._direction}"
        )
        renderer.string_put(20, 80, 0x888888, "Space: pause")
        renderer.string_put(20, 110, 0x888888, "G: game over")
        renderer.string_put(20, 140, 0x888888, "V: victory")
