from .mazeloader import MazeLoader
from .level import Level
from .entities import PacMan
from mazegenerator import MazeGenerator
import random
from typing import Literal


class Game():
    '''Class with the config and the state of the whole game'''
    cheating_keys = {
        "cheat", "invincible", "freeze", "life", "speed", "level"
        }

    def __init__(self, config: MazeLoader) -> None:
        self.config = config
        self.levels = self.level_generator()
        self.current_level = 0
        self.score = 0
        self.lives = config.datas["lives"]
        self.paused = False
        self.result: Literal["victory", "defeat"] | None = None
        self.set_timer()
        self.cheating_mode = False

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

    def set_timer(self) -> None:
        '''Define the starting time for each level'''
        self.timer = self.config.datas["level_max_time"]

    def update_timer(self, dt: float) -> None:
        '''Time before the end of the level'''
        self.timer -= dt
        if self.timer <= 0:
            self.game_end()

    def eat(self) -> None:
        '''Update the score according to gum eaten'''
        eaten = self.level.eat(self.level.pacman.pos)
        if eaten:
            self.score += self.config.datas[f"points_per_{eaten}"]
            if self.level.is_cleared():
                self.next_level()

    def next_level(self) -> None:
        '''Change level and quit if it was the last one'''
        if self.current_level + 1 == len(self.levels):
            self.game_end()
        else:
            self.current_level += 1
            self.set_timer()

    def game_end(self) -> None:
        '''Register the end of the game'''
        if self.lives == 0 or self.timer <= 0:
            self.result = "defeat"
        else:
            self.result = "victory"

    def handle_action(self, action: str) -> None:
        '''Apply an action asked by the player'''
        if action == "pause":
            self.paused = not self.paused
        elif self.paused:
            return
        elif action in PacMan.KEYS:
            self.level.pacman.set_next_direction(action)
        elif action in self.cheating_keys:
            self.cheating_mode = not self.cheating_mode
        elif action in self.cheating_keys and self.cheating_mode:
            ...

    def update(self, dt: float) -> None:
        '''One step of the game'''
        if self.paused or self.result:
            return
        self.update_timer(dt)

