"""Main loop of the game: fixed frame rate and window events."""

import time
from src.graphical.renderer import QUIT, Renderer
from src.graphical.screens.screen import Screen
from src.graphical.screens.menu import MenuScreen
from src.graphical.screens.game import GameScreen
from src.graphical.screens.pause import PauseScreen
from src.graphical.screens.highscores import HighscoresScreen
from src.graphical.screens.instructions import InstructionsScreen
from src.graphical.screens.end import EndScreen


# Number of frames per second, and duration of one frame in seconds.
FPS: int = 60
FRAME_TIME: float = 1.0 / FPS


class App:
    """Own the window and run the main loop at a fixed frame rate."""

    def __init__(self, width: int, height: int, title: str) -> None:
        """Open the window."""
        self._renderer = Renderer(width, height, title)
        self._running: bool = False
        # The screen currently shown; it receives keys and draws itself.
        self._screen: Screen = MenuScreen(self)

    def change_screen(self, screen: Screen) -> None:
        """Replace the current screen by another one."""
        self._screen = screen

    def quit(self) -> None:
        """Stop the main loop at the end of the current frame."""
        self._running = False

    def show_menu(self) -> None:
        """Go to the main menu."""
        self.change_screen(MenuScreen(self))

    def show_highscores(self) -> None:
        """Go to the highscores screen."""
        self.change_screen(HighscoresScreen(self))

    def show_instructions(self) -> None:
        """Go to the instructions screen."""
        self.change_screen(InstructionsScreen(self))

    def start_game(self) -> None:
        """Start a new game."""
        self.change_screen(GameScreen(self))

    def pause(self, game: Screen) -> None:
        """Pause the game; the pause screen keeps it to resume it."""
        self.change_screen(PauseScreen(self, game))

    def end_game(self, won: bool, score: int) -> None:
        """Show the end screen with the result of the game."""
        self.change_screen(EndScreen(self, won, score))

    def run(self) -> None:
        """Run the main loop until the window is closed."""
        self._running = True
        last = time.monotonic()
        try:
            while self._running:
                start = time.monotonic()
                # Time since the previous frame (about FRAME_TIME).
                dt = start - last
                last = start

                self._handle_events()
                self._screen.update(dt)
                self._draw()

                # Sleep what is left of the frame to keep a fixed rate.
                elapsed = time.monotonic() - start
                if elapsed < FRAME_TIME:
                    time.sleep(FRAME_TIME - elapsed)
        finally:
            # Always close the window, even if an error happened.
            self._renderer.close()

    def _handle_events(self) -> None:
        """Stop on window cross, give every other event to the screen."""
        for event in self._renderer.poll_events():
            if event.kind == QUIT:
                self.quit()
            else:
                self._screen.handle_event(event)

    def _draw(self) -> None:
        """Draw one frame."""
        self._renderer.clear()
        self._screen.draw(self._renderer)
        self._renderer.present()
