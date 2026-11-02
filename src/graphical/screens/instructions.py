"""Instructions screen: controls, rules and cheat keys."""

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

# Colors (MLX format 0xRRGGBB).
TITLE_COLOR: int = 0xFFFF00
TEXT_COLOR: int = 0xFFFFFF
HELP_COLOR: int = 0x888888

# Position of the first line and space between two lines, in pixels.
TEXT_X: int = 40
TEXT_Y: int = 30
LINE_HEIGHT: int = 34

# Each line: (color, text). An empty text is a blank line between sections.
INSTRUCTIONS: tuple[tuple[int, str], ...] = (
    (TITLE_COLOR, "CONTROLS"),
    (TEXT_COLOR, "Arrows / WASD: move Pac-Man"),
    (TEXT_COLOR, "Space: pause / resume"),
    (TEXT_COLOR, "Escape: back (in menus)"),
    (TEXT_COLOR, ""),
    (TITLE_COLOR, "RULES"),
    (TEXT_COLOR, "Eat every pacgum to clear the level."),
    (TEXT_COLOR, "Super-pacgums (corners) make ghosts edible for a while."),
    (TEXT_COLOR, "Eat edible ghosts for bonus points."),
    (TEXT_COLOR, "Touching a ghost costs one life."),
    (TEXT_COLOR, "Clear the level before the timer ends."),
    (TEXT_COLOR, "Clear every level to win the game."),
    (TEXT_COLOR, ""),
    (TITLE_COLOR, "CHEAT MODE"),
    (TEXT_COLOR, "C: enable cheat mode, then:"),
    (TEXT_COLOR, "1: invincible    2: freeze ghosts"),
    (TEXT_COLOR, "3: extra lives   4: speed up"),
    (TEXT_COLOR, "5: next level"),
)


class InstructionsScreen(Screen):
    """Explain the controls, the rules and the cheat keys."""

    def handle_event(self, event: InputEvent) -> None:
        """Go back to the menu on Escape."""
        if event.kind == KEY_DOWN and event.key == "escape":
            self._app.show_menu()

    def draw(self, renderer: Renderer) -> None:
        """Draw every line of the instructions, then the help line."""
        for index, (color, text) in enumerate(INSTRUCTIONS):
            # A blank line draws nothing but still takes its place.
            if text:
                y = TEXT_Y + index * LINE_HEIGHT
                renderer.string_put(TEXT_X, y, color, text)
        help_y = TEXT_Y + (len(INSTRUCTIONS) + 1) * LINE_HEIGHT
        renderer.string_put(TEXT_X, help_y, HELP_COLOR, "Escape: back to menu")
