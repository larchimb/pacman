from .mazeloader import MazeLoader
from mazegenerator import MazeGenerator
from .entities import PacMan, Hunter, Tricky, Randomly, Scary
import random


class Level():
    '''Class with all informations for a level'''
    def __init__(self, config: MazeLoader, maze: MazeGenerator) -> None:
        self._maze: list[list[int]] = maze.maze
        self._width = len(self._maze[0])
        self._height = len(self._maze)
        xpacman = (self._width - 1) // 2
        ypacman = (self._height - 1) // 2
        self.pacman = PacMan((xpacman, ypacman), 0.15)
        self.supergums = self.supergums_set_up()
        self.pacgums = self.pacgums_set_up(config.datas["pacgum"])
        self.ghosts = [
            Hunter((0, 0), 0.20),
            Tricky((self._width - 1, 0), 0.20),
            Randomly((self._width - 1, self._height - 1), 0.20),
            Scary((0, self._height - 1), 0.20)
        ]

    def get_excluded_cells(self) -> set[tuple[int, int]]:
        '''Return the cells where no pacgum can be placed'''
        closed_cells = set()
        for y, row in enumerate(self._maze):
            for x, cell in enumerate(row):
                if cell == 15:
                    closed_cells.add((x, y))
        excluded_cells = self.supergums | closed_cells | {self.pacman.pos}
        return excluded_cells

    def pacgums_set_up(self, nb_pacgums: int) -> set[tuple[int, int]]:
        '''To define and distribute the pacgum on the map'''
        excluded = self.get_excluded_cells()
        free_cells = [(x, y)
                      for y in range(self._height)
                      for x in range(self._width)
                      if (x, y) not in excluded]
        nb_pacgums = min(nb_pacgums, len(free_cells))
        return set(random.sample(free_cells, nb_pacgums))

    def supergums_set_up(self) -> set[tuple[int, int]]:
        '''To set up supergums starts'''
        return {
            (0, 0), (self._width - 1, 0),
            (0, self._height - 1),
            (self._width - 1, self._height - 1)
            }

    def is_cleared(self) -> bool:
        '''To check if the level is finished'''
        if not self.supergums and not self.pacgums:
            return True
        return False

    def eat(self, gum: tuple[int, int]) -> str | None:
        '''To remove gum from the map'''
        if gum in self.pacgums:
            self.pacgums.discard(gum)
            return "pacgum"
        elif gum in self.supergums:
            self.supergums.discard(gum)
            return "supergum"
        return None
