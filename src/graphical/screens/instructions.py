"""Instructions screen: controls, rules and cheat keys."""

from src.graphical.renderer import KEY_DOWN, InputEvent, Renderer
from src.graphical.screens.screen import Screen

TITLE_COLOR: int = 0xFFFF00
TEXT_COLOR: int = 0xFFFFFF
LINE_HEIGHT: int = 34

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
        """Draw the instructions as a block centered in the window."""
        self._draw_background(renderer)
        lines = INSTRUCTIONS + ((TEXT_COLOR, ""),)
        widest = max(renderer.text_width(text) for _, text in lines)
        left = (renderer.width - widest) // 2
        top = (renderer.height - len(lines) * LINE_HEIGHT) // 2
        for index, (color, text) in enumerate(lines):
            if text:
                y = top + index * LINE_HEIGHT
                renderer.string_put(left, y, color, text)
        super().draw(renderer)
