"""Main loop of the game: fixed frame rate and window events."""

import time
from src.graphical.renderer import KEY_DOWN, QUIT, Renderer


# Number of frames per second, and duration of one frame in seconds.
FPS: int = 60
FRAME_TIME: float = 1.0 / FPS

# Keys that move Pac-Man: arrows and WASD give the same direction.
DIRECTION_KEYS: dict[str, str] = {
    "up": "up", "w": "up",
    "down": "down", "s": "down",
    "left": "left", "a": "left",
    "right": "right", "d": "right",
}


class App:
    """Own the window and run the main loop at a fixed frame rate."""

    def __init__(self, width: int, height: int, title: str) -> None:
        """Open the window."""
        self._renderer = Renderer(width, height, title)
        # The loop runs while this is True; set it to False to stop.
        self._running: bool = False
        # Last direction asked by the player (sent to the game later).
        self._direction: str = "none"

    def run(self) -> None:
        """Run the main loop until the window is closed."""
        self._running = True
        try:
            while self._running:
                start = time.monotonic()

                self._handle_events()
                self._draw()

                # sleep what is left of the frame to keep a fixed rate.
                elapsed = time.monotonic() - start
                if elapsed < FRAME_TIME:
                    time.sleep(FRAME_TIME - elapsed)
        finally:
            self._renderer.close()

    def _handle_events(self) -> None:
        """Read the window events and stop on cross or Escape."""
        for event in self._renderer.poll_events():
            if event.kind == QUIT:
                self._running = False
            elif event.kind == KEY_DOWN and event.key == "escape":
                self._running = False
            elif event.kind == KEY_DOWN and event.key in DIRECTION_KEYS:
                self._direction = DIRECTION_KEYS[event.key]

    def _draw(self) -> None:
        """Draw one frame."""
        self._renderer.clear()
        self._renderer.string_put(20, 20, 0xFFFF00, "Pac-Man")
        self._renderer.string_put(
            20, 50, 0xFFFFFF, f"Direction: {self._direction}"
        )
        self._renderer.present()
