"""Throwaway test of the FakeGame: print the board as text."""

from src.graphical.fake_game import CLOSED_CELL, FakeGame

game = FakeGame()
level = game.level
ghosts = {ghost.pos for ghost in level.ghosts}

# maze[y][x]: a list of rows, so loop on y first, then on x.
for y in range(level.height):
    line = ""
    for x in range(level.width):
        if (x, y) == level.pacman.pos:
            line += "P"
        elif (x, y) in ghosts:
            line += "G"
        elif level.maze[y][x] == CLOSED_CELL:
            line += "#"
        elif (x, y) in level.pacgums:
            line += "."
        else:
            line += " "
    print(line)

print(f"pacman {level.pacman}, {len(level.pacgums)} pacgums")
print(f"supergums {sorted(level.supergums)}")
