"""Base class of every screen of the game."""


from typing import TYPE_CHECKING

from src.graphical.renderer import InputEvent, Renderer

if TYPE_CHECKING:
    from src.graphical.app import App


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
