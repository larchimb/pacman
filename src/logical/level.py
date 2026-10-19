from .mazeloader import MazeLoader
from mazegenerator import MazeGenerator
import random

class Level():
    '''Class with all informations for a level'''
    def __init__(self, config: MazeLoader, maze: MazeGenerator) -> None:
        self._maze: list[list[int]] = maze.maze
        self._width = len(self._maze[0])
        self._height = len(self._maze)
        xpacman =  int(
        self._width / 2 if not self._width % 2 == 0 else (self._width / 2) - 1
            )
        ypacman = int(
        self._height / 2 if self._height % 2 else (self._height / 2) - 1
        )
        self.pacman = (xpacman, ypacman)
        self.pacgums = self.pacgums_distribution(config.datas["pacgum"])
        
    def get_excluded_cells(self) -> set[tuple[int, int]]:
        '''Return the cells where no pacgum can be placed'''
        corners = {(0, 0), (self._width - 1, 0),
                   (0, self._height - 1),
                   (self._width - 1, self._height - 1)}
        closed_cells = set()
        for y, row in enumerate(self._maze):
            for x, cell in enumerate(row):
                if cell == 15:
                    closed_cells.add((x, y))
        excluded_cells = corners | closed_cells | {self.pacman}
        return excluded_cells

    def pacgums_distribution(self, nb_pacgums: int) -> set[tuple[int, int]]:
        '''To define and distribute the pacgum on the map'''
        excluded = self.get_excluded_cells()
        free_cells = [(x, y)
                      for y in range(self._height)
                      for x in range(self._width)
                      if (x, y) not in excluded]
        nb_pacgums = min(nb_pacgums, len(free_cells))
        return set(random.sample(free_cells, nb_pacgums))
