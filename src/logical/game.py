from .mazeloader import MazeLoader
from .level import Level
from .entities import PacMan
from mazegenerator import MazeGenerator
import random
from typing import Literal
import json


class Game():
    '''Class with the config and the state of the whole game'''
    cheating_keys = {
        "invincible", "freeze", "life", "speed", "level"
        }

    def __init__(self, config: MazeLoader) -> None:
        self.config = config
        self.rng = random.Random()
        self.levels = self.level_generator()
        self.current_level = 0
        self.score = 0
        self.lives = config.datas["lives"]
        self.paused = False
        self.result: Literal["victory", "defeat"] | None = None
        self.set_level_timer()
        self.cheating_mode = False
        self.frozen = False
        self.supertime = False
        self.max_life = 99

    def generate_maze(self, size: tuple[int, int],
                      seed: int, level: int) -> MazeGenerator:
        '''Generate a valid maze, retrying once with another seed'''
        for _ in range(2):
            try:
                maze = MazeGenerator(size, perfect=False, seed=seed)
                if (len(maze.maze) == size[1]
                        and all(len(row) == size[0] for row in maze.maze)):
                    return maze
                print(f"[GENERATOR ERROR]: level {level}, wrong maze size")
            except Exception as e:
                print(f"[GENERATOR ERROR]: level {level}, {e}")
            seed = self.rng.randint(1, 100000)
        raise RuntimeError(
            f"[GENERATOR ERROR]: unable to generate the maze of level {level}")

    def level_generator(self) -> list[Level]:
        '''Complete all information about the levels from MazeLoader'''
        levels: list[Level] = []
        for i, (x, y) in enumerate(self.config.datas["levels"], start=1):
            seed = (self.config.datas["seed"] if i == 1
                    else self.rng.randint(1, 100000))
            levels.append(Level(self.config,
                                self.generate_maze((x, y), seed, i),
                                self.rng))
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

    def update_supergum_timer(self, dt: float) -> None:
        '''Time before the end of the supertime'''
        self.supergum_timer -= dt
        if self.supergum_timer <= 0:
            self.deactivate_power()

    def eat(self) -> None:
        '''Eat the gum under Pac-Man, score it and apply its effect'''
        eaten = self.level.eat(self.level.pacman.cell)
        if eaten:
            self.score += self.config.datas[f"points_per_{eaten}"]
            if self.level.is_cleared():
                self.pass_level()
            elif eaten == "supergum":
                self.activate_power()

    def activate_power(self) -> None:
        '''To activate pacman power, slow down the ghosts'''
        self.supertime = True
        self.supergum_timer: float = 12
        for g in self.level.ghosts:
            g.weak = True
            g.step_time = 1.5 * g.basic_step

    def deactivate_power(self) -> None:
        '''To deactivate pacman power, speed up the ghosts'''
        self.supertime = False
        for g in self.level.ghosts:
            g.weak = False
            g.step_time = g.basic_step

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
            self.supertime = False

    def game_end(self) -> None:
        '''Register the end of the game'''
        if self.lives == 0 or self.level_timer <= 0:
            self.result = "defeat"
        else:
            self.result = "victory"

    def add_life(self) -> None:
        '''Add a life to Pacman'''
        if self.lives < self.max_life:
            self.lives += 1

    def lose_life(self) -> None:
        '''Lose a life to Pacman'''
        self.lives -= 1
        if self.lives <= 0:
            self.game_end()

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

    def collision(self) -> None:
        '''To deal with collision between Pacman and a ghost'''
        for g in self.level.ghosts:
            if self.level.pacman.cell == g.cell:
                if g.waiting_time > 0:
                    continue
                elif g.weak:
                    self.score += self.config.datas["points_per_ghost"]
                    g.respawn()
                    g.waiting_time = 5.0
                elif self.level.pacman.invincible:
                    continue
                else:
                    self.lose_life()
                    self.level.pacman.respawn()
                    for ghost in self.level.ghosts:
                        ghost.respawn()
                    break

    def update(self, dt: float) -> None:
        '''One step of the game'''
        if self.paused or self.result:
            return
        self.update_level_timer(dt)
        if self.supertime:
            self.update_supergum_timer(dt)
        level = self.level
        pacman = level.pacman
        ghosts = level.ghosts
        pacman.tick(dt)
        self.eat()
        if self.level is not level:
            return
        self.collision()
        if not self.frozen:
            for ghost in ghosts:
                ghost.tick(dt)
                self.collision()

    def save_score(self, name: str) -> bool:
        '''Add the score to the highscores and save the top 10'''
        name = name.strip()
        if not MazeLoader.is_valid_entry(name, self.score):
            return False
        highscores = self.config.datas["highscore"]
        highscores.append({"name": name, "score": self.score})
        self.config.datas["highscore"] = MazeLoader.top_ten(highscores)
        path = self.config.path_to_highscore
        try:
            with open(path, "w", encoding="utf-8") as f:
                json.dump({"highscores": self.config.datas["highscore"]},
                          f, indent=2)
        except OSError as e:
            print(f"[SAVE ERROR]: cannot write '{path}': {e}")
            return False
        return True
