"""Board of the game: walls, gums, Pac-Man and ghosts."""

from src.graphical.renderer import Image, Renderer

# Size of one cell in pixels (same as the sprites in assets/).
CELL_SIZE: int = 44
# Thickness of a wall bar in pixels.
WALL_THICKNESS: int = 4
# Arcade blue.
WALL_COLOR: int = 0x2121DE
# Height of the HUD at the top of the window; the board goes under it.
HUD_HEIGHT: int = 80

# Bit of each wall in a cell (same values as Entity.DIRECTIONS).
NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8
# Cell with its 4 walls closed (the "42" logo).
CLOSED_CELL: int = 15


class BoardView:
    """Draw a level, cell by cell."""

    def __init__(self, renderer: Renderer) -> None:
        """Create the wall images once (creating them is slow)."""
        # Horizontal bar for N and S walls, vertical bar for W and E.
        self._h_wall: Image = renderer.new_filled_image(
            CELL_SIZE + WALL_THICKNESS, WALL_THICKNESS, WALL_COLOR
        )
        self._v_wall: Image = renderer.new_filled_image(
            WALL_THICKNESS, CELL_SIZE + WALL_THICKNESS, WALL_COLOR
        )
        # A full cell for the "42" logo.
        self._full_cell: Image = renderer.new_filled_image(
            CELL_SIZE, CELL_SIZE, WALL_COLOR
        )

    def draw(self, renderer: Renderer, maze: list[list[int]]) -> None:
        """Draw the walls of every cell, centered under the HUD."""
        # maze[y][x]: the number of rows is the height.
        width = len(maze[0])
        height = len(maze)
        # Split the free space in two equal margins to center the board.
        offset_x = (renderer.width - width * CELL_SIZE) // 2
        offset_y = HUD_HEIGHT + (
            renderer.height - HUD_HEIGHT - height * CELL_SIZE
        ) // 2
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                # Top-left pixel of the cell (x, y).
                px = offset_x + x * CELL_SIZE
                py = offset_y + y * CELL_SIZE
                self._draw_cell(renderer, cell, px, py)

    def _draw_cell(
        self, renderer: Renderer, cell: int, px: int, py: int
    ) -> None:
        """Draw the walls of one cell whose top-left pixel is (px, py)."""
        if cell == CLOSED_CELL:
            renderer.put_image(self._full_cell, px, py)
            return
        # A wall is shared by 2 cells: each bar is centered on the border
        # (half inside, half outside), so both cells draw it at the same
        # place and it stays WALL_THICKNESS thick.
        half = WALL_THICKNESS // 2
        if cell & NORTH:
            renderer.put_image(self._h_wall, px - half, py - half)
        if cell & SOUTH:
            renderer.put_image(
                self._h_wall, px - half, py + CELL_SIZE - half
            )
        if cell & WEST:
            renderer.put_image(self._v_wall, px - half, py - half)
        if cell & EAST:
            renderer.put_image(
                self._v_wall, px + CELL_SIZE - half, py - half
            )
