"""Pause screen: resume the game or go back to the menu."""

from typing import TYPE_CHECKING

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

if TYPE_CHECKING:
    from src.graphical.app import App


class PauseScreen(Screen):
    """Shown on top of a paused game."""

    def __init__(self, app: "App", game: Screen) -> None:
        """Keep the paused game to resume it later."""
        super().__init__(app)
        # The paused game: shown again, unchanged, when resuming.
        self._game = game

    def handle_event(self, event: InputEvent) -> None:
        """Resume on Space, go to the menu on M."""
        if event.kind != KEY_DOWN:
            return
        if event.key == "space":
            self._app.change_screen(self._game)
        elif event.key == "m":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw the pause menu."""
        renderer.string_put(20, 20, 0xFFFF00, "PAUSE")
        renderer.string_put(20, 50, 0xFFFFFF, "Space: resume")
        renderer.string_put(20, 80, 0xFFFFFF, "M: main menu")
