"""End screen: game over or victory, then the player types a name."""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer, Image
from src.graphical.pixel_font import new_pixel_image, pixel_rows
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App

MAX_NAME_LENGTH: int = 10

WIN_COLOR: int = 0x00FF00
LOSE_COLOR: int = 0xFF0000
TEXT_COLOR: int = 0xFFFFFF
NAME_COLOR: int = 0xFFFF00
HELP_COLOR: int = 0x888888
TITLE_BLOCK: int = 10
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
        text, color = ("VICTORY", WIN_COLOR) if won else (
            "GAME OVER", LOSE_COLOR)
        self._title_rows = pixel_rows(text)
        self._title: Image = new_pixel_image(
            app.renderer, self._title_rows, color, TITLE_BLOCK
        )

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
        """Draw the big title, the score and the name, centered."""
        self._draw_background(renderer)
        title_width = len(self._title_rows[0]) * TITLE_BLOCK
        title_height = len(self._title_rows) * TITLE_BLOCK
        message = (
            "Congratulations, you cleared every level!" if self._won else ""
        )
        cursor = "_" if len(self._name) < MAX_NAME_LENGTH else ""
        lines: list[tuple[int, str]] = [
            (TEXT_COLOR, message),
            (TEXT_COLOR, f"Score: {self._score}"),
            (TEXT_COLOR, ""),
            (TEXT_COLOR, "Enter your name:"),
            (NAME_COLOR, self._name + cursor),
            (TEXT_COLOR, "")
        ]
        block_height = title_height + (len(lines) + 1) * LINE_HEIGHT
        top = (renderer.height - block_height) // 2
        renderer.put_image(
            self._title, (renderer.width - title_width) // 2, top
        )
        lines_top = top + title_height + LINE_HEIGHT
        for index, (color, text) in enumerate(lines):
            if text:
                renderer.string_put(
                    self._center_x(renderer, text),
                    lines_top + index * LINE_HEIGHT,
                    color,
                    text,
                )
        super().draw(renderer)
