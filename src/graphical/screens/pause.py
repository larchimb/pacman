"""Pause screen: resume the game or go back to the menu."""

from typing import TYPE_CHECKING, Callable

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App

# Colors (MLX format 0xRRGGBB).
TITLE_COLOR: int = 0xFFFF00
SELECTED_COLOR: int = 0xFFFF00
NORMAL_COLOR: int = 0xFFFFFF
HELP_COLOR: int = 0x888888

# Position of the pause menu, around the center of the 1440 x 960 window.
PAUSE_X: int = 620
PAUSE_Y: int = 380
LINE_HEIGHT: int = 50


class PauseScreen(Screen):
    """Pause menu shown on top of the frozen game."""

    def __init__(self, app: "App", game: Screen) -> None:
        """Keep the paused game and build the menu options."""
        super().__init__(app)
        self._game = game
        self._options: list[tuple[str, Callable[[], None]]] = [
            ("Resume", self._resume),
            ("Main menu", app.show_menu)
        ]
        self._selected: int = 0

    def _resume(self) -> None:
        """Go back to the paused game, unchanged."""
        self._app.change_screen(self._game)

    def handle_event(self, event: InputEvent) -> None:
        """Move with up/down (or W/S), run on Enter, resume on Space."""
        if event.kind != KEY_DOWN:
            return
        count = len(self._options)
        if event.key in ("up", "w"):
            self._selected = (self._selected - 1) % count
        elif event.key in ("down", "s"):
            self._selected = (self._selected + 1) % count
        elif event.key == "return":
            _, action = self._options[self._selected]
            action()
        elif event.key == "space":
            self._resume()

    def draw(self, renderer: Renderer) -> None:
        """Draw the frozen game, then the pause menu on top of it."""
        self._game.draw(renderer)
        renderer.string_put(PAUSE_X, PAUSE_Y, TITLE_COLOR, "PAUSE")
        for index, (text, _) in enumerate(self._options):
            y = PAUSE_Y + (index + 1) * LINE_HEIGHT
            if index == self._selected:
                renderer.string_put(PAUSE_X, y, SELECTED_COLOR, "> " + text)
            else:
                renderer.string_put(PAUSE_X, y, NORMAL_COLOR, "  " + text)
        help_y = PAUSE_Y + (len(self._options) + 1) * LINE_HEIGHT + 20
        renderer.string_put(PAUSE_X, help_y, HELP_COLOR, "Space: resume")
