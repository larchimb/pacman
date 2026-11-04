"""Pause screen: resume the game or go back to the menu."""

from typing import TYPE_CHECKING, Callable

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App

TITLE_COLOR: int = 0xFFFF00
SELECTED_COLOR: int = 0xFFFF00
NORMAL_COLOR: int = 0xFFFFFF
HELP_COLOR: int = 0x888888


LINE_HEIGHT: int = 50
BOX_WIDTH: int = 300
BOX_HEIGHT: int = 280
BOX_PADDING: int = 60
BOX_COLOR: int = 0x000000
FRAME_COLOR: int = 0x2121DE
FRAME_THICKNESS: int = 4


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
        self._frame = app.renderer.new_filled_image(
            BOX_WIDTH + 2 * FRAME_THICKNESS,
            BOX_HEIGHT + 2 * FRAME_THICKNESS,
            FRAME_COLOR
        )
        self._box = app.renderer.new_filled_image(
            BOX_WIDTH, BOX_HEIGHT, BOX_COLOR
        )

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
        width = int(self._app.width / 2 - 100)
        height = int(self._app.height / 2 - 100)
        box_x = width - BOX_PADDING
        box_y = height - BOX_PADDING
        renderer.put_image(
            self._frame, box_x - FRAME_THICKNESS, box_y - FRAME_THICKNESS
        )
        renderer.put_image(self._box, box_x, box_y)

        renderer.string_put(width, height, TITLE_COLOR, "PAUSE")
        for index, (text, _) in enumerate(self._options):
            y = height + (index + 1) * LINE_HEIGHT
            if index == self._selected:
                renderer.string_put(width, y, SELECTED_COLOR, "> " + text)
            else:
                renderer.string_put(width, y, NORMAL_COLOR, "  " + text)
