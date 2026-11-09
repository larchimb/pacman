"""Highscores screen: the 10 best scores, the player's one highlighted."""

from typing import TYPE_CHECKING, Any

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App

TITLE_COLOR: int = 0xFFFF00
TEXT_COLOR: int = 0xFFFFFF
PLAYER_COLOR: int = 0xFFFF00
LINE_HEIGHT: int = 50
TABLE_WIDTH: int = 400


class HighscoresScreen(Screen):
    """Show the top 10 scores, the player's new score highlighted."""

    def __init__(
        self, app: "App", player: tuple[str, int] | None = None
    ) -> None:
        """Keep the scores and find the player's line once."""
        super().__init__(app)
        self._scores: list[dict[str, Any]] = app.config.datas["highscore"]
        self._player = player
        self._highlight = self._find_player()

    def _find_player(self) -> int | None:
        """Return the index of the player's score in the table, or None."""
        if self._player is None:
            return None
        name, score = self._player
        for index, entry in enumerate(self._scores):
            if entry["name"] == name and entry["score"] == score:
                return index
        return None

    def handle_event(self, event: InputEvent) -> None:
        """Go back to the menu on Escape."""
        if event.kind == KEY_DOWN and event.key == "escape":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw the title and the table centered, then the help line."""
        self._draw_background(renderer)
        rows = max(len(self._scores), 1)
        missing = self._player is not None and self._highlight is None
        total = rows + 2 + (2 if missing else 0)
        top = (renderer.height - total * LINE_HEIGHT) // 2
        title = "HIGHSCORES"
        renderer.string_put(
            self._center_x(renderer, title), top, TITLE_COLOR, title
        )
        first_y = top + 2 * LINE_HEIGHT
        if not self._scores:
            text = "No score yet"
            renderer.string_put(
                self._center_x(renderer, text), first_y, TEXT_COLOR, text
            )
        left = (renderer.width - TABLE_WIDTH) // 2
        for index, entry in enumerate(self._scores):
            y = first_y + index * LINE_HEIGHT
            mine = index == self._highlight
            color = PLAYER_COLOR if mine else TEXT_COLOR
            name = f"{index + 1}. {entry['name']}"
            score = str(entry["score"])
            if mine:
                arrow_x = left - renderer.text_width("> ")
                renderer.string_put(arrow_x, y, color, "> ")
            renderer.string_put(left, y, color, name)
            score_x = left + TABLE_WIDTH - renderer.text_width(score)
            renderer.string_put(score_x, y, color, score)
        if missing and self._player is not None:
            text = f"Your score: {self._player[1]} (not in the top 10)"
            y = first_y + (rows + 1) * LINE_HEIGHT
            renderer.string_put(
                self._center_x(renderer, text), y, PLAYER_COLOR, text
            )
        super().draw(renderer)
