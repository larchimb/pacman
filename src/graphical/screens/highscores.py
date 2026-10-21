"""Highscores screen: the best scores."""

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen


class HighscoresScreen(Screen):
    """Show the top 10 scores."""

    def handle_event(self, event: InputEvent) -> None:
        """Go back to the menu on Escape."""
        if event.kind == KEY_DOWN and event.key == "escape":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw the scores (placeholder text until the highscore table)."""
        renderer.string_put(20, 20, 0xFFFF00, "HIGHSCORES")
        renderer.string_put(20, 50, 0xFFFFFF, "No score yet")
        renderer.string_put(20, 140, 0x888888, "Escape: back to menu")
