"""Board of the game: walls, gums, Pac-Man and ghosts."""
from typing import TYPE_CHECKING

from src.graphical.renderer import Image, Pixels, Renderer

if TYPE_CHECKING:
    from src.logical.level import Level
    from src.logical.entities import Entity

CELL_SIZE: int = 50
# Thickness of a wall bar in pixels.
WALL_THICKNESS: int = 4
WALL_COLOR: int = 0x2121DE
PACGUM_SIZE: int = 10
SUPERGUM_SIZE: int = 20
GUM_COLOR: int = 0xFFB8AE
SPRITE_SIZE: int = 44
ASSETS_DIR: str = "assets"
# Sprite of Pac-Man for each direction of the logic (Entity.DIRECTIONS).
PACMAN_SPRITES: dict[str, str] = {
    "N": "pacman_up.png",
    "E": "pacman_right.png",
    "S": "pacman_down.png",
    "W": "pacman_left.png",
}
# Before his first move, direction is None: he looks to the right.
PACMAN_DEFAULT: str = "E"
GHOST_SPRITES: tuple[str, ...] = (
    "ghost_red.png", "ghost_pink.png", "ghost_blue.png", "ghost_orange.png",
)
GHOST_WEAK_SPRITE: str = "ghost_edible.png"


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
        self._full_cell: Image = renderer.new_filled_image(
            CELL_SIZE, CELL_SIZE, WALL_COLOR
        )
        self._offset_x: int = 0
        self._offset_y: int = 0
        self._pacgum: Image = self._new_dot(renderer, PACGUM_SIZE)
        self._supergum: Image = self._new_dot(renderer, SUPERGUM_SIZE)
        self._pacman: dict[str, Pixels] = {
            direction: renderer.opaque_pixels(
                renderer.load_image(f"{ASSETS_DIR}/{name}")
            )
            for direction, name in PACMAN_SPRITES.items()
        }
        self._ghosts: list[Pixels] = [
            renderer.opaque_pixels(renderer.load_image(f"{ASSETS_DIR}/{name}"))
            for name in GHOST_SPRITES
        ]
        self._ghost_weak: Pixels = renderer.opaque_pixels(
            renderer.load_image(f"{ASSETS_DIR}/{GHOST_WEAK_SPRITE}")
        )

    def draw(self, renderer: Renderer, level: "Level") -> None:
        """Draw the walls, then the gums, centered under the HUD."""
        maze = level._maze
        width = len(maze[0])
        height = len(maze)
        self._offset_x = (renderer.width - width * CELL_SIZE) // 2
        self._offset_y = HUD_HEIGHT + (
            renderer.height - HUD_HEIGHT - height * CELL_SIZE
        ) // 2
        for y, row in enumerate(maze):
            for x, cell in enumerate(row):
                px, py = self._cell_pixel((x, y))
                self._draw_cell(renderer, cell, px, py)
        for pos in level.pacgums:
            self._put_centered(
                renderer, self._pacgum, PACGUM_SIZE, self._cell_pixel(pos)
            )
        for pos in level.supergums:
            self._put_centered(
                renderer, self._supergum, SUPERGUM_SIZE, self._cell_pixel(pos)
            )
        pacman = level.pacman
        direction = pacman.direction or PACMAN_DEFAULT
        self._put_sprite(
            renderer, self._pacman[direction], self._entity_pixel(pacman)
        )
        for index, ghost in enumerate(level.ghosts):
            if ghost.waiting_time > 0:
                continue
            image = self._ghost_weak if ghost.weak else self._ghosts[index]
            self._put_sprite(
                renderer, image, self._entity_pixel(ghost)
            )

    def _cell_pixel(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Return the top-left pixel of the cell at pos."""
        x, y = pos
        return (
            self._offset_x + x * CELL_SIZE,
            self._offset_y + y * CELL_SIZE,
        )

    def _entity_pixel(self, entity: "Entity") -> tuple[int, int]:
        """Return the top-left pixel of an entity sliding between 2 cells."""
        t = min(entity.elapsed / entity.step_time, 1.0)
        (x0, y0), (x1, y1) = entity.prev_pos, entity.pos
        x = x0 + (x1 - x0) * t
        y = y0 + (y1 - y0) * t
        return (
            round(self._offset_x + x * CELL_SIZE),
            round(self._offset_y + y * CELL_SIZE),
        )

    def _put_centered(
        self, renderer: Renderer, image: Image, size: int,
        pixel: tuple[int, int],
    ) -> None:
        """Draw a size x size image in the middle of the cell at pixel."""
        px, py = pixel
        margin = (CELL_SIZE - size) // 2
        renderer.put_image(image, px + margin, py + margin)

    def _put_sprite(
        self, renderer: Renderer, pixels: Pixels, pixel: tuple[int, int]
    ) -> None:
        """Draw a sprite's colored pixels in the middle of the cell."""
        px, py = pixel
        margin = (CELL_SIZE - SPRITE_SIZE) // 2
        renderer.put_pixels(pixels, px + margin, py + margin)

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

    @staticmethod
    def _new_dot(renderer: Renderer, size: int) -> Image:
        """Create a disc of size x size pixels on a black image."""
        image = renderer.new_image(size, size)
        center = (size - 1) / 2
        radius = size / 2
        for y in range(size):
            for x in range(size):
                if (x - center) ** 2 + (y - center) ** 2 <= radius ** 2:
                    renderer.image_pixel_put(image, x, y, GUM_COLOR)
        return image
