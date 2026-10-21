"""End screen: game over or victory."""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App


class EndScreen(Screen):
    """Shown when the game is over, won or lost."""

    def __init__(self, app: "App", won: bool, score: int) -> None:
        """Keep the result of the game to display it."""
        super().__init__(app)
        self._won = won
        self._score = score

    def handle_event(self, event: InputEvent) -> None:
        """Go back to the menu on Enter (name input comes later)."""
        if event.kind == KEY_DOWN and event.key == "return":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw the result and the score."""
        if self._won:
            renderer.string_put(20, 20, 0x00FF00, "VICTORY")
        else:
            renderer.string_put(20, 20, 0xFF0000, "GAME OVER")
        renderer.string_put(20, 50, 0xFFFFFF, f"Score: {self._score}")
        renderer.string_put(20, 140, 0x888888, "Enter: back to menu")
