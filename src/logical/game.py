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
        self.score = 0
        self.lives = config.datas["lives"]
        self.paused = False

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

    def eat(self) -> None:
        '''Update the score according to gum eaten'''
        eaten = self.level.eat(self.level.pacman.pos)
        if eaten:
            self.score =+ self.config.datas[f"points_per_{eaten}"]
            if self.level.is_cleared():
                self.next_level()

    def next_level(self) -> None:
        '''Change level and quit if it was the last one'''
        self.current_level += 1
        if self.current_level == len(self.levels):
            self.game_end()

    def game_end(self) -> None:
        '''Close the game and go to the hisghscore menu'''

    def handle_action(self, action: str) -> None:
        '''Apply an action asked by the player'''
        if action == "pause":
            self.paused = not self.paused
        elif self.paused:
            return
        # elif action in PacMan.KEYS:
        #     self.level.pacman.get_next_direction()

    def update(self) -> None:
        '''One step of the game'''
        ...
