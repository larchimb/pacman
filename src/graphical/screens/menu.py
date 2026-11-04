"""Main menu screen."""

from typing import TYPE_CHECKING, Callable

from src.graphical.renderer import KEY_DOWN, InputEvent, Image, Renderer
from src.graphical.screens.screen import Screen


if TYPE_CHECKING:
    from src.graphical.app import App


TITLE_COLOR: int = 0xFFFF00
SELECTED_COLOR: int = 0xFFFF00
NORMAL_COLOR: int = 0xFFFFFF
HELP_COLOR: int = 0x888888


OPTIONS_X: int = 40
OPTIONS_Y: int = 140
LINE_HEIGHT: int = 50

TITLE_PIXELS: tuple[str, ...] = (
    "####. .###. .#### ... #...# .###. #...#",
    "#...# #...# #.... ... ##.## #...# ##..#",
    "####. ##### #.... ### #.#.# ##### #.#.#",
    "#.... #...# #.... ... #...# #...# #..##",
    "#.... #...# .#### ... #...# #...# #...#",
)
TITLE_BLOCK: int = 12


class MenuScreen(Screen):
    """Main menu: start, highscores, instructions, exit."""

    def __init__(self, app: "App") -> None:
        """Build the list of options, the first one is selected."""
        super().__init__(app)
        self._options: list[tuple[str, Callable[[], None]]] = [
            ("Start Game", app.start_game),
            ("Highscores", app.show_highscores),
            ("Instructions", app.show_instructions),
            ("Exit", app.quit)
        ]
        self._selected: int = 0
        self._title: Image = self._new_title(app.renderer)

    def handle_event(self, event: InputEvent) -> None:
        """Move with up/down (or W/S), run on Enter, quit on Escape."""
        if event.kind != KEY_DOWN:
            return
        count = len(self._options)
        if event.key in ("up", "w"):
            self._selected = (self._selected - 1) % count
        elif event.key in ("down", "s"):
            self._selected = (self._selected + 1) % count
        elif event.key == "return":
            _, action = self._options[self._selected]
            action()
        elif event.key == "escape":
            self._app.quit()

    @staticmethod
    def _new_title(renderer: Renderer) -> Image:
        """Create the big title image from TITLE_PIXELS."""
        width = len(TITLE_PIXELS[0]) * TITLE_BLOCK
        height = len(TITLE_PIXELS) * TITLE_BLOCK
        image = renderer.new_image(width, height)
        for row, line in enumerate(TITLE_PIXELS):
            for col, char in enumerate(line):
                if char != "#":
                    continue
                for y in range(TITLE_BLOCK):
                    for x in range(TITLE_BLOCK):
                        renderer.image_pixel_put(
                            image,
                            col * TITLE_BLOCK + x,
                            row * TITLE_BLOCK + y,
                            TITLE_COLOR,
                        )
        return image

    def draw(self, renderer: Renderer) -> None:
        """Draw the big title and the options centered in the window."""
        title_width = len(TITLE_PIXELS[0]) * TITLE_BLOCK
        title_height = len(TITLE_PIXELS) * TITLE_BLOCK
        block_height = title_height + (len(self._options) + 1) * LINE_HEIGHT
        top = (renderer.height - block_height) // 2
        renderer.put_image(
            self._title, (renderer.width - title_width) // 2, top
        )
        options_top = top + title_height + LINE_HEIGHT
        for index, (text, _) in enumerate(self._options):
            x = self._center_x(renderer, text)
            y = options_top + index * LINE_HEIGHT
            if index == self._selected:
                arrow_x = x - renderer.text_width("> ")
                renderer.string_put(arrow_x, y, SELECTED_COLOR, "> ")
                renderer.string_put(x, y, SELECTED_COLOR, text)
            else:
                renderer.string_put(x, y, NORMAL_COLOR, text)
