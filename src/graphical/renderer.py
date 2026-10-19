"""MLX-compatible rendering layer built on top of pygame.

The subject only allows a graphical library "similar to MLX": every
function we use must have an MLX equivalent. This module is the ONLY
place in the project that imports pygame, and it only exposes
operations that MLX also provides. The rest of the game must go
through the Renderer class and never call pygame directly.

pygame call                          MLX equivalent
-----------------------------------  ---------------------------------
pygame.display.init() + font.init()  mlx_init()
pygame.display.set_mode()            mlx_new_window()
pygame.display.set_caption()         title argument of mlx_new_window()
pygame.display.Info()                mlx_get_screen_size()
pygame.Surface((w, h))               mlx_new_image()
pygame.image.load()                  mlx_png_file_to_image()
Surface.set_at() on an image         write in mlx_get_data_addr() buffer
Surface.set_at() on the window       mlx_pixel_put()
window.blit(image, (x, y))           mlx_put_image_to_window()
window.fill(black)                   mlx_clear_window()
pygame.font.Font(None) + render      mlx_string_put()
pygame.display.flip()                mlx_do_sync()
pygame.event.get()                   mlx_hook() / mlx_loop_hook()
pygame.quit()                        mlx_destroy_window() + mlx_release()

Colors are given as 0xRRGGBB integers, exactly like in MLX.
"""

from dataclasses import dataclass

import pygame

# Size of the text drawn by string_put. MLX only has one fixed font,
# so we never change it.
FONT_SIZE: int = 20

QUIT: str = "quit"
KEY_DOWN: str = "key_down"
KEY_UP: str = "key_up"

# Special keys translated to simple names. Letters and digits are
# translated directly (their pygame code is their ASCII code, like the
# X11 keysyms received by MLX).
_SPECIAL_KEYS: dict[int, str] = {
    pygame.K_UP: "up",
    pygame.K_DOWN: "down",
    pygame.K_LEFT: "left",
    pygame.K_RIGHT: "right",
    pygame.K_ESCAPE: "escape",
    pygame.K_SPACE: "space",
    pygame.K_RETURN: "return",
    pygame.K_BACKSPACE: "backspace",
}


class RendererError(Exception):
    """Raised when the graphical layer cannot do what was asked."""


@dataclass(frozen=True)
class InputEvent:
    """A window event, independent from pygame."""

    kind: str
    key: str = ""


def to_rgb(color: int) -> tuple[int, int, int]:
    """Convert an MLX-style 0xRRGGBB color to an (r, g, b) tuple."""
    return ((color >> 16) & 0xFF, (color >> 8) & 0xFF, color & 0xFF)


def _key_name(code: int) -> str:
    """Translate a pygame key code to the name used by the game."""
    if code in _SPECIAL_KEYS:
        return _SPECIAL_KEYS[code]
    if pygame.K_a <= code <= pygame.K_z or pygame.K_0 <= code <= pygame.K_9:
        return chr(code)
    return ""


class Renderer:
    """Window and drawing primitives, limited to what MLX can do."""

    def __init__(self, width: int, height: int, title: str) -> None:
        """Open the game window (mlx_init + mlx_new_window)."""
        try:
            pygame.display.init()
            pygame.font.init()
            self._window = pygame.display.set_mode((width, height))
            pygame.display.set_caption(title)
            self._font = pygame.font.Font(None, FONT_SIZE)
        except pygame.error as err:
            pygame.quit()
            raise RendererError(f"cannot open the window: {err}") from err
        self.width: int = width
        self.height: int = height
        self._images: dict[str, pygame.Surface] = {}

    @staticmethod
    def get_screen_size() -> tuple[int, int]:
        """Return the size of the monitor (mlx_get_screen_size)."""
        pygame.display.init()
        info = pygame.display.Info()
        return (info.current_w, info.current_h)

    def new_image(self, width: int, height: int) -> pygame.Surface:
        """Create a black image in memory (mlx_new_image)."""
        return pygame.Surface((width, height))

    def new_filled_image(
        self, width: int, height: int, color: int
    ) -> pygame.Surface:
        """Create an image of a single color."""
        image = self.new_image(width, height)
        rgb = to_rgb(color)
        for y in range(height):
            for x in range(width):
                image.set_at((x, y), rgb)
        return image

    def image_pixel_put(
        self, image: pygame.Surface, x: int, y: int, color: int
    ) -> None:
        """Write one pixel in an image (mlx_get_data_addr buffer)."""
        if 0 <= x < image.get_width() and 0 <= y < image.get_height():
            image.set_at((x, y), to_rgb(color))

    def load_image(self, path: str) -> pygame.Surface:
        """Load a PNG file as an image (mlx_png_file_to_image)."""
        if path not in self._images:
            try:
                self._images[path] = pygame.image.load(path)
            except (pygame.error, FileNotFoundError) as err:
                raise RendererError(
                    f"cannot load image '{path}': {err}"
                ) from err
        return self._images[path]

    def clear(self) -> None:
        """Fill the whole window with black (mlx_clear_window)."""
        self._window.fill((0, 0, 0))

    def pixel_put(self, x: int, y: int, color: int) -> None:
        """Draw one pixel in the window (mlx_pixel_put)."""
        self._window.set_at((x, y), to_rgb(color))

    def put_image(self, image: pygame.Surface, x: int, y: int) -> None:
        """Draw an image in the window (mlx_put_image_to_window)."""
        self._window.blit(image, (x, y))

    def string_put(self, x: int, y: int, color: int, text: str) -> None:
        """Write text in the window (mlx_string_put)."""
        surface = self._font.render(text, True, to_rgb(color))
        self._window.blit(surface, (x, y))

    def present(self) -> None:
        """Show everything drawn since the last call (mlx_do_sync)."""
        pygame.display.flip()

    def poll_events(self) -> list[InputEvent]:
        """Return the window events received since the last call."""
        events: list[InputEvent] = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                events.append(InputEvent(QUIT))
            elif event.type == pygame.KEYDOWN:
                events.append(InputEvent(KEY_DOWN, _key_name(event.key)))
            elif event.type == pygame.KEYUP:
                events.append(InputEvent(KEY_UP, _key_name(event.key)))
        return events

    def close(self) -> None:
        """Close the window and free everything (mlx_destroy_window)."""
        self._images.clear()
        pygame.quit()
