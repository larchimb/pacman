"""Base class of every screen of the game."""


from typing import TYPE_CHECKING

from src.graphical.renderer import InputEvent, Renderer
from src.paths import resource_path

if TYPE_CHECKING:
    from src.graphical.app import App

BACKGROUND: str = resource_path("assets/background.png")


class Screen:
    """One state of the game: reacts to keys, updates, draws itself."""

    def __init__(self, app: "App") -> None:
        """Keep a link to the app, to ask it to change screen."""
        self._app = app

    def handle_event(self, event: InputEvent) -> None:
        """React to one window event. Does nothing by default."""

    def update(self, dt: float) -> None:
        """Advance the screen by dt seconds. Does nothing by default."""

    def draw(self, renderer: Renderer) -> None:
        """Draw the screen. Does nothing by default."""
        middle = int(self._app.width / 2)
        height = self._app.height - 50
        renderer.string_put(
            int(middle - 8 * self._app.character),
            height,
            0x888888,
            "Escape: back to menu")

    def _draw_background(self, renderer: Renderer) -> None:
        """Draw the background image, made for the fixed window size."""
        renderer.put_image(renderer.load_image(BACKGROUND), 0, 0)

    @staticmethod
    def _center_x(renderer: Renderer, text: str) -> int:
        """Return the x where the text must start to be centered."""
        return (renderer.width - renderer.text_width(text)) // 2
