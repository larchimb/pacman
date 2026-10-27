from .mazeloader import MazeLoader
from .level import Level
from .entities import PacMan
from mazegenerator import MazeGenerator
import random
from typing import Literal


class Game():
    '''Class with the config and the state of the whole game'''
    cheating_keys = {
        "invincible", "freeze", "life", "speed", "level"
        }

    def __init__(self, config: MazeLoader) -> None:
        self.config = config
        self.levels = self.level_generator()
        self.current_level = 0
        self.score = 0
        self.lives = config.datas["lives"]
        self.paused = False
        self.result: Literal["victory", "defeat"] | None = None
        self.set_level_timer()
        self.cheating_mode = False
        self.frozen = False

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

    def set_level_timer(self) -> None:
        '''Define the starting time for each level'''
        self.level_timer = self.config.datas["level_max_time"]

    def update_level_timer(self, dt: float) -> None:
        '''Time before the end of the level'''
        self.level_timer -= dt
        if self.level_timer <= 0:
            self.game_end()

    def eat(self) -> None:
        '''Update the score according to gum eaten'''
        eaten = self.level.eat(self.level.pacman.pos)
        if eaten:
            self.score += self.config.datas[f"points_per_{eaten}"]
            if self.level.is_cleared():
                self.pass_level()

    def maintain_cheats(self) -> None:
        '''Report all the cheats on the next pacman'''
        next_level = self.levels[self.current_level + 1]
        next_level.pacman.step_time = self.level.pacman.step_time
        next_level.pacman.invincible = self.level.pacman.invincible

    def pass_level(self) -> None:
        '''Change level and quit if it was the last one'''
        if self.current_level + 1 == len(self.levels):
            self.game_end()
        else:
            self.maintain_cheats()
            self.current_level += 1
            self.set_level_timer()

    def game_end(self) -> None:
        '''Register the end of the game'''
        if self.lives == 0 or self.level_timer <= 0:
            self.result = "defeat"
        else:
            self.result = "victory"

    def add_life(self) -> None:
        '''Add a life to Pacman'''
        if self.lives < 99:
            self.lives += 1

    def activate_cheat(self, action: str) -> None:
        '''Activate or deactivate the cheat code choosen'''
        if action == "invincible":
            self.level.pacman.invincible = not self.level.pacman.invincible
        elif action == "freeze":
            self.frozen = not self.frozen
        elif action == "life":
            self.add_life()
        elif action == "speed":
            self.level.pacman.cheat_speed()
        elif action == "level":
            self.pass_level()

    def handle_action(self, action: str) -> None:
        '''Apply an action asked by the player'''
        if action == "pause":
            self.paused = not self.paused
        elif self.paused:
            return
        elif action in PacMan.KEYS:
            self.level.pacman.set_next_direction(action)
        elif action == "cheat":
            self.cheating_mode = not self.cheating_mode
        elif action in self.cheating_keys and self.cheating_mode:
            self.activate_cheat(action)

    def update(self, dt: float) -> None:
        '''One step of the game'''
        if self.paused or self.result:
            return
        self.update_level_timer(dt)
