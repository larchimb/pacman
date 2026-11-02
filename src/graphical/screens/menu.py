"""Main menu screen."""

from typing import TYPE_CHECKING, Callable

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen


if TYPE_CHECKING:
    from src.graphical.app import App


# Colors of the menu (MLX format 0xRRGGBB).
TITLE_COLOR: int = 0xFFFF00
SELECTED_COLOR: int = 0xFFFF00
NORMAL_COLOR: int = 0xFFFFFF
HELP_COLOR: int = 0x888888


# Position of the first option and space between two options, in pixels.
OPTIONS_X: int = 40
OPTIONS_Y: int = 140
LINE_HEIGHT: int = 50


class MenuScreen(Screen):
    """Main menu: start, highscores, instructions, exit."""

    def __init__(self, app: "App") -> None:
        """Build the list of options, the first one is selected."""
        super().__init__(app)
        # Each option: the text shown and the method called on Enter.
        # No () after the methods: we store them, we don't call them yet.
        self._options: list[tuple[str, Callable[[], None]]] = [
            ("Start Game", app.start_game),
            ("Highscores", app.show_highscores),
            ("Instructions", app.show_instructions),
            ("Exit", app.quit)
        ]
        # Index of the selected option in self._options.
        self._selected: int = 0

    def handle_event(self, event: InputEvent) -> None:
        """Move with up/down (or W/S), run on Enter, quit on Escape."""
        if event.kind != KEY_DOWN:
            return
        count = len(self._options)
        if event.key in ("up", "w"):
            # Modulo: going up from the first option goes to the last one.
            self._selected = (self._selected - 1) % count
        elif event.key in ("down", "s"):
            self._selected = (self._selected + 1) % count
        elif event.key == "return":
            # Get the method of the selected option, then call it.
            _, action = self._options[self._selected]
            action()
        elif event.key == "escape":
            self._app.quit()

    def draw(self, renderer: Renderer) -> None:
        """Draw the title and the options, the selected one in yellow."""
        renderer.string_put(OPTIONS_X, 40, TITLE_COLOR, "PAC-MAN")
        for index, (text, _) in enumerate(self._options):
            y = OPTIONS_Y + index * LINE_HEIGHT
            if index == self._selected:
                renderer.string_put(OPTIONS_X, y, SELECTED_COLOR, "> " + text)
            else:
                renderer.string_put(OPTIONS_X, y, NORMAL_COLOR, "  " + text)
        help_y = OPTIONS_Y + len(self._options) * LINE_HEIGHT + 20
        renderer.string_put(
            OPTIONS_X, help_y, HELP_COLOR, "Up/Down: choose  Enter: select"
        )
