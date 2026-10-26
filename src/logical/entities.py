class Entity():
    '''Mother class for Pacman and ghosts'''
    DIRECTIONS = {"N": (0, -1, 1), "E": (1, 0, 2),
                  "S": (0, 1, 4), "W": (-1, 0, 8)}

    def __init__(self, start: tuple[int, int], step_time: float) -> None:
        self.start = start
        self.pos = start
        self.step_time = step_time
        self.direction: str | None = None
        self.next_direction: str | None = None

    def can_move(self, maze: list[list[int]], direction: str) -> bool:
        '''Check if there is no wall in this direction'''
        x, y = self.pos
        return not (maze[y][x] & self.DIRECTIONS[direction][2])

    def possible_directions(self, maze: list[list[int]]) -> list[str]:
        '''Return all the directions without wall'''
        return [d for d in self.DIRECTIONS if self.can_move(maze, d)]

    def move(self, maze: list[list[int]]) -> None:
        '''Move one cell, turning to next_direction if possible'''
        if self.next_direction and self.can_move(maze, self.next_direction):
            self.direction = self.next_direction
        if self.direction and self.can_move(maze, self.direction):
            dx, dy, _ = self.DIRECTIONS[self.direction]
            self.pos = (self.pos[0] + dx, self.pos[1] + dy)


class PacMan(Entity):
    '''Class for Pacman's entity'''
    KEYS = {"up", "down", "left", "right"}

    def __init__(self, start: tuple[int, int], step_time: float) -> None:
        super().__init__(start, step_time)

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


class Hunter(Entity):
    def __init__(self, start: tuple[int, int], step_time: float) -> None:
        super().__init__(start, step_time)

    def get_next_direction(self) -> None:
        '''To find the next direction accordind to the keyboard command'''
        ...


class Tricky(Entity):
    def __init__(self, start: tuple[int, int], step_time: float) -> None:
        super().__init__(start, step_time)

    def get_next_direction(self) -> None:
        '''To find the next direction accordind to the keyboard command'''
        ...


class Randomly(Entity):
    def __init__(self, start: tuple[int, int], step_time: float) -> None:
        super().__init__(start, step_time)

    def get_next_direction(self) -> None:
        '''To find the next direction accordind to the keyboard command'''
        ...


class Scary(Entity):
    def __init__(self, start: tuple[int, int], step_time: float) -> None:
        super().__init__(start, step_time)

    def get_next_direction(self) -> None:
        '''To find the next direction accordind to the keyboard command'''
        ...
