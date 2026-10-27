from abc import ABC, abstractmethod


class Entity():
    '''Mother class for Pacman and ghosts'''
    DIRECTIONS = {"N": (0, -1, 1), "E": (1, 0, 2),
                  "S": (0, 1, 4), "W": (-1, 0, 8)}

    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        self.maze = maze
        self.start = start
        self.pos = start
        self.basic_step = step_time
        self.step_time = step_time
        self.direction: str | None = None
        self.next_direction: str | None = None
        self.elapsed: float = 0

    def can_move(self, direction: str) -> bool:
        '''Check if there is no wall in this direction'''
        x, y = self.pos
        return not (self.maze[y][x] & self.DIRECTIONS[direction][2])

    def move(self) -> None:
        '''Move one cell, turning to next_direction if possible'''
        if self.next_direction and self.can_move(self.next_direction):
            self.direction = self.next_direction
        if self.direction and self.can_move(self.direction):
            dx, dy, _ = self.DIRECTIONS[self.direction]
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)

    def tick(self, dt: float) -> None:
        '''Move one cell when enough time has passed'''
        self.elapsed += dt
        if self.elapsed >= self.step_time:
            self.elapsed -= self.step_time
            self.move()


class PacMan(Entity):
    '''Class for Pacman's entity'''
    KEYS = {"up", "down", "left", "right"}

    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)
        self.invincible = False

    def set_next_direction(self, action: str) -> None:
        '''To find the next direction accordind to the keyboard command'''
        if action == "up":
            self.next_direction = "N"
        elif action == "down":
            self.next_direction = "S"
        elif action == "left":
            self.next_direction = "W"
        elif action == "right":
            self.next_direction = "E"

    def cheat_speed(self) -> None:
        '''Switch the speed value between normal and cheat mode'''
        if not self.basic_step == self.step_time:
            self.step_time = self.basic_step
        else:
            self.step_time /= 2


class Ghost(Entity, ABC):
    '''Class for ghost's entities'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)
        self.weak = False

    def possible_directions(self) -> list[str]:
        '''Return all the directions without wall'''
        return [d for d in self.DIRECTIONS if self.can_move(d)]

    @abstractmethod
    def get_next_direction(self, pacman: tuple[int, int]) -> None:
        '''To find the next direction depending of the ghost's kind'''


class Hunter(Ghost):
    '''The hunter's class for hunting the pacman'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self, pacman: tuple[int, int]) -> None:
        '''Find a direct way to the pacman'''
        ...


class Tricky(Ghost):
    '''The tricky class for tricking the pacman'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self, pacman: tuple[int, int]) -> None:
        '''Try to find a way to trick Pacman'''
        ...


class Randomly(Ghost):
    '''The random class define random moves for a ghost'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self, pacman: tuple[int, int]) -> None:
        '''Choose randomly a direction'''
        self.possible_directions()


class Scary(Ghost):
    '''The scary class is for the ghost who hunt and flew the Pacman'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self, pacman: tuple[int, int]) -> None:
        '''Try to find Pacman except if it is too close'''
        ...
