"""Main menu screen."""

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen


class MenuScreen(Screen):
    """Main menu: start, highscores, instructions, exit."""

    def handle_event(self, event: InputEvent) -> None:
        """Start a game on Enter, quit on Escape."""
        if event.kind != KEY_DOWN:
            return
        if event.key == "return":
            self._app.start_game()
        elif event.key == "escape":
            self._app.quit()

    def draw(self, renderer: Renderer) -> None:
        """Draw the menu."""
        renderer.string_put(20, 20, 0xFFFF00, "MENU")
        renderer.string_put(20, 50, 0xFFFFFF, "Enter: start")
        renderer.string_put(20, 80, 0xFFFFFF, "Escape: quit")
