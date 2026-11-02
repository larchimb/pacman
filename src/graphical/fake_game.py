"""Temporary fake Game with the same attributes as the real one."""

import random
from dataclasses import dataclass

from mazegenerator import MazeGenerator

# Value of a cell with its 4 walls closed (the "42" logo).
CLOSED_CELL: int = 15
# Number of pacgums placed on the board.
NB_PACGUMS: int = 50
# Directions used by the logic (Entity.DIRECTIONS in entities.py).
DIRECTIONS: tuple[str, ...] = ("N", "E", "S", "W")


@dataclass
class FakeEntity:
    """Pac-Man or a ghost: a position in cells and a direction."""

    pos: tuple[int, int]
    direction: str | None = None


class FakeLevel:
    """One level built like Luc's Level, with a public maze."""

    def __init__(self, width: int, height: int, seed: int) -> None:
        """Generate the maze and place everything on it."""
        self.width: int = width
        self.height: int = height
        # The generator is not typed (Any): annotate what we receive.
        self.maze: list[list[int]] = MazeGenerator(
            (width, height), seed=seed
        ).maze
        self.pacman = FakeEntity(((width - 1) // 2, (height - 1) // 2), "E")
        corners = [
            (0, 0), (width - 1, 0), (width - 1, height - 1), (0, height - 1)
        ]
        # Same order as Luc: the index gives the color of the ghost
        # (0 red, 1 pink, 2 blue, 3 orange).
        self.ghosts: list[FakeEntity] = [FakeEntity(c) for c in corners]
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
            random.sample(free_cells, min(NB_PACGUMS, len(free_cells)))
        )


class FakeGame:
    """Fake Game: same attribute names as src/logical/game.py."""

    def __init__(self) -> None:
        """Start on the biggest level, with a fixed seed."""
        self.level = FakeLevel(23, 19, seed=42)
        self.score: int = 0
        self.lives: int = 3
        self.current_level: int = 0
        self.timer: float = 0.0
        self.result: str | None = None

    def handle_action(self, action: str) -> None:
        """Turn Pac-Man (only to test the sprites)."""
        if action in DIRECTIONS:
            self.level.pacman.direction = action

    def update(self, dt: float) -> None:
        """Advance the timer by dt seconds."""
        self.timer += dt
