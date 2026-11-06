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
BOX_HEIGHT: int = 260
BOX_PADDING: int = 40
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
        """Draw the frozen game, then the pause menu centered on top."""
        self._game.draw(renderer)
        box_x = (renderer.width - BOX_WIDTH) // 2
        box_y = (renderer.height - BOX_HEIGHT) // 2
        renderer.put_image(
            self._frame, box_x - FRAME_THICKNESS, box_y - FRAME_THICKNESS
        )
        renderer.put_image(self._box, box_x, box_y)
        top = box_y + BOX_PADDING
        renderer.string_put(
            self._center_x(renderer, "PAUSE"), top, TITLE_COLOR, "PAUSE"
        )
        for index, (text, _) in enumerate(self._options):
            x = self._center_x(renderer, text)
            y = top + (index + 1) * LINE_HEIGHT
            if index == self._selected:
                arrow_x = x - renderer.text_width("> ")
                renderer.string_put(arrow_x, y, SELECTED_COLOR, "> ")
                renderer.string_put(x, y, SELECTED_COLOR, text)
            else:
                renderer.string_put(x, y, NORMAL_COLOR, text)

