from abc import ABC, abstractmethod
from random import randint
from collections import deque


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

    def respawn(self) -> None:
        '''To make the entity respawn at his original place'''
        self.pos = self.start
        self.direction = None
        self.next_direction = None
        self.elapsed = 0


class PacMan(Entity):
    '''Class for Pacman's entity'''
    KEYS = {"up", "down", "left", "right"}

    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)
        self.invincible = False

    def set_next_direction(self, action: str) -> None:
        '''To find the next direction according to the keyboard command'''
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
        self.shortest_path: str | None = None

    def possible_directions(self) -> list[str]:
        '''Return all the directions without wall'''
        return [d for d in self.DIRECTIONS if self.can_move(d)]

    def set_pacman(self, pacman: PacMan) -> None:
        '''Link the ghost to the Pac-Man it reacts to'''
        self.pacman = pacman

    def move(self) -> None:
        '''Choose the next direction, then move one cell'''
        self.get_next_direction()
        super().move()

    def go_to(self, goal: tuple[int, int]) -> None:
        '''Turn toward the first step of the shortest path to goal'''
        self.find_shortest_path(goal)
        if self.shortest_path:
            self.next_direction = self.shortest_path[0]
        self.shortest_path = None

    @abstractmethod
    def get_next_direction(self) -> None:
        '''To find the next direction depending of the ghost's kind'''

    def get_flee_direction(self) -> None:
        '''To find the next direction to escape from Pacman'''
        self.find_shortest_path(self.pacman.pos)
        if self.shortest_path:
            toward = self.shortest_path[0]
            escapes = [d for d in self.possible_directions() if d != toward]
            if escapes:
                self.next_direction = escapes[randint(0, len(escapes) - 1)]
            else:
                self.next_direction = toward
        self.shortest_path = None

    def respawn(self) -> None:
        '''To change the specificities of the ghost'''
        super().respawn()
        self.weak = False
        self.step_time = self.basic_step

    def find_shortest_path(self, goal: tuple[int, int]) -> None:
        '''Compute the shortest path from the ghost to goal'''
        moves = [
            (0, -1, 1, 'N'), (1, 0, 2, 'E'),
            (0, 1, 4, 'S'), (-1, 0, 8, 'W')
            ]   # dx, dy, wall code, letter
        start = self.pos
        prev: dict = {start: None}
        queue = deque([start])
        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                break
            for dx, dy, wall, letter in moves:
                nx, ny = x + dx, y + dy
                if (0 <= nx < len(self.maze[0]) and 0 <= ny < len(self.maze)
                        and (self.maze[y][x] & wall) == 0
                        and (nx, ny) not in prev):
                    prev[(nx, ny)] = ((x, y), letter)
                    queue.append((nx, ny))
        letters = []
        cur = goal
        while prev[cur] is not None:
            parent, letter = prev[cur]
            letters.append(letter)
            cur = parent
        self.shortest_path = ''.join(reversed(letters))


class Hunter(Ghost):
    '''The hunter's class for hunting the pacman'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self) -> None:
        '''Find a direct way to the pacman'''
        if self.weak:
            self.get_flee_direction()
            return
        self.go_to(self.pacman.pos)


class Tricky(Ghost):
    '''The tricky class for tricking the pacman'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self) -> None:
        '''Find the shortest path to Pac-Man's predicted position.'''
        if self.weak:
            self.get_flee_direction()
            return
        px, py = self.pacman.pos
        goal = (px, py)
        direction = self.pacman.direction
        if direction:
            dx, dy, _ = self.DIRECTIONS[direction]
            for i in range(4, 0, -1):
                x, y = (px + dx * i, py + dy * i)
                if (0 <= x < len(self.maze[0]) and 0 <= y < len(self.maze)
                        and self.maze[y][x] != 15) and (x, y) != self.pos:
                    goal = (x, y)
                    break
        self.go_to(goal)


class Randomly(Ghost):
    '''The random class define random moves for a ghost'''
    OPPOSITE = {"N": "S", "S": "N", "E": "W", "W": "E"}

    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)

    def get_next_direction(self) -> None:
        '''Choose randomly a direction, without turning back if possible'''
        if self.weak:
            self.get_flee_direction()
            return
        directions = self.possible_directions()
        if self.direction:
            forward = [d for d in directions
                       if d != self.OPPOSITE[self.direction]]
            if forward:
                directions = forward
        self.next_direction = directions[randint(0, len(directions) - 1)]


class Scary(Ghost):
    '''The scary class is for the ghost who hunt and flee the Pacman'''
    def __init__(self, maze: list[list[int]],
                 start: tuple[int, int], step_time: float) -> None:
        super().__init__(maze, start, step_time)
        self.way_back = False

    def get_next_direction(self) -> None:
        '''Try to find Pacman except if it is too close'''
        if self.weak:
            self.get_flee_direction()
            return
        if self.pos == self.start:
            self.way_back = False
        if self.way_back:
            self.go_to(self.start)
        else:
            self.find_shortest_path(self.pacman.pos)
            if self.shortest_path:
                self.next_direction = self.shortest_path[0]
            if self.shortest_path and len(self.shortest_path) < 6:
                self.way_back = True
            self.shortest_path = None
