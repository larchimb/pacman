"""End screen: game over or victory, then the player types a name"""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App

MAX_NAME_LENGTH: int = 10

# Colors (MLX format 0xRRGGBB).
WIN_COLOR: int = 0x00FF00
LOSE_COLOR: int = 0xFF0000
TEXT_COLOR: int = 0xFFFFFF
NAME_COLOR: int = 0xFFFF00
HELP_COLOR: int = 0x888888

# Position of the first line and space between two lines, in pixels.
END_X: int = 480
END_Y: int = 300
LINE_HEIGHT: int = 50


class EndScreen(Screen):
    """Show the result and the score, let the player type a name."""

    def __init__(self, app: "App", won: bool, score: int) -> None:
        """Keep the result of the game, start with an emty name."""
        super().__init__(app)
        self._won = won
        self._score = score
        self._name: str = ""
        self._shift: bool = False

    def handle_event(self, event: InputEvent) -> None:
        """Type the name, Enter to save it, Escape to skip."""
        if event.key == "shift":
            self._shift = event.kind == KEY_DOWN
            return
        if event.kind != KEY_DOWN:
            return
        if event.key == "return":
            self._validate()
        elif event.key == "escape":
            self._app.show_menu()
        elif event.key == "backspace":
            self._name = self._name[:-1]
        elif len(self._name) < MAX_NAME_LENGTH:
            self._add_char(event.key)

    def _add_char(self, key: str) -> None:
        """Add a letter, a digit or a space at the end of the name."""
        if key == "space":
            self._name += " "
        elif len(key) == 1 and key.isalnum():
            self._name += key.upper() if self._shift else key

    def _validate(self) -> None:
        """Save the score if the name is not empty."""
        name = self._name.strip()
        if name:
            self._app.save_score(name, self._score)

    def draw(self, renderer: Renderer) -> None:
        """Draw the result, the score and the name being typed."""
        if self._won:
            renderer.string_put(END_X, END_Y, WIN_COLOR, "VICTORY")
            renderer.string_put(
                END_X, END_Y + LINE_HEIGHT, TEXT_COLOR,
                "Congratulations, you cleared every level!"
            )
        else:
            renderer.string_put(END_X, END_Y, LOSE_COLOR, "GAME OVER")

        y = END_Y + 2 * LINE_HEIGHT
        renderer.string_put(
            END_X, y + LINE_HEIGHT, TEXT_COLOR, "Enter your name:"
        )

        cursor = "_" if len(self._name) < MAX_NAME_LENGTH else ""
        renderer.string_put(
            END_X, y + 2 * LINE_HEIGHT, NAME_COLOR, self._name + cursor
        )
        renderer.string_put(
            END_X, y + 3 * LINE_HEIGHT + 20, HELP_COLOR,
            "Enter: save    Escape: skip"
        )
