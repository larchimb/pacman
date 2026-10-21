"""Instructions screen: how to play."""

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen


class InstructionsScreen(Screen):
    """Explain the controls and the goal of the game."""

    def handle_event(self, event: InputEvent) -> None:
        """Go back to the menu on Escape."""
        if event.kind == KEY_DOWN and event.key == "escape":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw the instructions (placeholder text for now)."""
        renderer.string_put(20, 20, 0xFFFF00, "INSTRUCTIONS")
        renderer.string_put(20, 50, 0xFFFFFF, "Arrows / WASD: move")
        renderer.string_put(20, 80, 0xFFFFFF, "Space: pause")
        renderer.string_put(20, 140, 0x888888, "Escape: back to menu")
