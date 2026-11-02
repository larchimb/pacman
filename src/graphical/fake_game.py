"""Fake Game for the graphics until the real one works (temporary)."""

import random
from dataclasses import dataclass

from mazegenerator import MazeGenerator

# Value of the closed cells that draw the "42" in the maze.
CLOSED_CELL: int = 15


@dataclass
class FakeEntity:
    """Pac-Man or a ghost: a cell position and a direction."""

    pos: tuple[int, int]
    direction: str | None = None


class FakeLevel:
    """One level: the maze and what is placed in it, like Luc's Level."""

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Generate the real maze, then place the elements."""
        # The annotation tells mypy the type (the generator is untyped: Any).
        self.maze: list[list[int]] = MazeGenerator(
            (width, height), seed=seed
        ).maze
        self.pacman = FakeEntity(((width - 1) // 2, (height - 1) // 2), "E")
        corners = [
            (0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)
        ]
        # Same order as Luc: Hunter (red), Tricky (pink), Randomly (blue),
        # Scary (orange): the index gives the color.
        self.ghosts = [FakeEntity(corner) for corner in corners]
        self.supergums: set[tuple[int, int]] = set(corners)
        free_cells = [
            (x, y)
            for y in range(height)
            for x in range(width)
            if self.maze[y][x] != CLOSED_CELL
            and (x, y) not in self.supergums
            and (x, y) != self.pacman.pos
        ]
        self.pacgums: set[tuple[int, int]] = set(
            random.sample(free_cells, min(50, len(free_cells)))
        )


class FakeGame:
    """Same attributes and entry points as Luc's Game, without the rules."""

    def __init__(self) -> None:
        """Create one level of the biggest size (23 x 19)."""
        self.level = FakeLevel(23, 19, seed=42)
        self.score: int = 0
        self.lives: int = 3
        self.current_level: int = 0
        self.timer: float = 0.0
        self.result: str | None = None

    def handle_action(self, action: str) -> None:
        """Turn Pac-Man on a direction action, to test the sprites."""
        if action in ("N", "E", "S", "W"):
            self.level.pacman.direction = action

    def update(self, dt: float) -> None:
        """Only count the time: the real rules are in Luc's Game."""
        self.timer += dt
