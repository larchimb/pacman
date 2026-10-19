from .mazeloader import MazeLoader
from .level import Level
from mazegenerator import MazeGenerator
import random


class Game():
    '''Class with the config and the state of the whole game'''
    def __init__(self, config: MazeLoader) -> None:
        self.config = config
        self.levels = self.level_generator()
        self.current_level = 0

    def level_generator(self) -> list[Level]:
        '''Complete all information about the levels from MazeLoader'''
        levels: list[Level] = []
        for i, (x, y) in enumerate(self.config.datas["levels"], start=1):
            seed = (self.config.datas["seed"] if i == 1
                    else random.randint(0, 1000))
            levels.append(Level(self.config,
                                MazeGenerator((x, y), seed=seed)))
        return levels

    @property
    def level(self) -> Level:
        '''The level currently played'''
        return self.levels[self.current_level]
