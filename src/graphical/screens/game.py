"""Game screen: the board and the HUD."""

from typing import TYPE_CHECKING

from src.graphical.renderer import (
    KEY_DOWN, InputEvent, Renderer, Image, Pixels
)
from src.graphical.screens.screen import Screen
from src.logical.game import Game
from src.logical.entities import Entity
if TYPE_CHECKING:
    from src.graphical.app import App


DIRECTION_KEYS: dict[str, str] = {
    "up": "up", "w": "up",
    "down": "down", "s": "down",
    "left": "left", "a": "left",
    "right": "right", "d": "right",
}

CELL_SIZE: int = 52
WALL_THICKNESS: int = 4
WALL_COLOR: int = 0x2121DE
PACGUM_SIZE: int = 10
SUPERGUM_SIZE: int = 20
GUM_COLOR: int = 0xFFB8AE
SPRITE_SIZE: int = 44
ASSETS_DIR: str = "assets"
PACMAN_SPRITES: dict[str, str] = {
    "N": "pacman_up.png",
    "E": "pacman_right.png",
    "S": "pacman_down.png",
    "W": "pacman_left.png",
}
PACMAN_DEFAULT: str = "E"
GHOST_SPRITES: tuple[str, ...] = (
    "ghost_red.png", "ghost_pink.png", "ghost_blue.png", "ghost_orange.png",
)
GHOST_WEAK_SPRITE: str = "ghost_edible.png"

HUD_HEIGHT: int = 50
HUD_COLOR: int = 0xFFFFFF
HUD_Y: int = 28
HUD_MARGIN: int = 40

NORTH: int = 1
EAST: int = 2
SOUTH: int = 4
WEST: int = 8
CLOSED_CELL: int = 15


class GameScreen(Screen):
    """Screen shown while playing."""

    def __init__(self, app: "App", game: Game) -> None:
        """Start with no direction asked yet."""
        super().__init__(app)
        self._direction: str = "none"
        self.game = game
        self.renderer = app._renderer
        self._h_wall: Image = self.renderer.new_filled_image(
            CELL_SIZE + WALL_THICKNESS, WALL_THICKNESS, WALL_COLOR
        )
        self._v_wall: Image = self.renderer.new_filled_image(
            WALL_THICKNESS, CELL_SIZE + WALL_THICKNESS, WALL_COLOR
        )
        self._full_cell: Image = self.renderer.new_filled_image(
            CELL_SIZE, CELL_SIZE, WALL_COLOR
        )
        self._offset_x: int = 0
        self._offset_y: int = 0
        self._pacgum: Image = self._new_dot(self.renderer, PACGUM_SIZE)
        self._supergum: Image = self._new_dot(self.renderer, SUPERGUM_SIZE)
        self._pacman: dict[str, Pixels] = {
            direction: self.renderer.opaque_pixels(
                self.renderer.load_image(f"{ASSETS_DIR}/{name}")
            )
            for direction, name in PACMAN_SPRITES.items()
        }
        self._ghosts: list[Pixels] = [
            self.renderer.opaque_pixels(self.renderer.load_image(f"{ASSETS_DIR}/{name}"))
            for name in GHOST_SPRITES
        ]
        self._ghost_weak: Pixels = self.renderer.opaque_pixels(
            self.renderer.load_image(f"{ASSETS_DIR}/{GHOST_WEAK_SPRITE}")
        )

    def handle_event(self, event: InputEvent) -> None:
        """Pause on Space, remember the last direction key."""
        if event.kind != KEY_DOWN:
            return
        action = ""
        if event.key == "space":
            self._app.pause(self)
        elif event.key in DIRECTION_KEYS:
            action = DIRECTION_KEYS[event.key]
        elif event.key == "c":
            action = "cheat"
        elif event.key == "1":
            action = "invincible"
        elif event.key == "2":
            action = "freeze"
        elif event.key == "3":
            action = "life"
        elif event.key == "4":
            action = "speed"
        elif event.key == "5":
            action = "level"
        self.game.handle_action(action)

    def update(self, dt: float) -> None:
        '''The main loop for animation'''
        self.game.update(dt)
        if self.game.result == "victory":
            self._app.end_game(True, self.game.score)
        elif self.game.result =="defeat":
            self._app.end_game(False, self.game.score)

    def draw(self, renderer: Renderer) -> None:
        """Draw the walls, then the gums, centered under the HUD."""
        level = self.game.levels[self.game.current_level]
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
                self._draw_cell(cell, px, py)
        for pos in level.pacgums:
            self._put_centered(
                self._pacgum, PACGUM_SIZE, self._cell_pixel(pos)
            )
        for pos in level.supergums:
            self._put_centered(
                self._supergum, SUPERGUM_SIZE, self._cell_pixel(pos)
            )
        pacman = level.pacman
        direction = pacman.direction or PACMAN_DEFAULT
        self._put_sprite(
            self._pacman[direction], self._entity_pixel(pacman)
        )
        for index, ghost in enumerate(level.ghosts):
            if ghost.waiting_time > 0:
                continue
            image = self._ghost_weak if ghost.weak else self._ghosts[index]
            self._put_sprite(
                image, self._entity_pixel(ghost)
            )
        if self.game.cheating_mode:
            renderer.string_put(
                650,
                self._app.height - 50,
                0xFFFFFF,
                "Cheat code : ON   1: Invincible   2: Freeze   3: Extra Life  "
                " 4: Speed   5: Level Up"
                )
        else:
            renderer.string_put(
                650,
                self._app.height - 50,
                0xFFFFFF,
                "Cheat code : OFF"
                )
        self._draw_hud(self.renderer)

    def _cell_pixel(self, pos: tuple[int, int]) -> tuple[int, int]:
        """Return the top-left pixel of the cell at pos."""
        x, y = pos
        return (
            self._offset_x + x * CELL_SIZE,
            self._offset_y + y * CELL_SIZE,
        )

    def _entity_pixel(self, entity: Entity) -> tuple[int, int]:
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
        self, image: Image, size: int,
        pixel: tuple[int, int],
    ) -> None:
        """Draw a size x size image in the middle of the cell at pixel."""
        px, py = pixel
        margin = (CELL_SIZE - size) // 2
        self.renderer.put_image(image, px + margin, py + margin)

    def _put_sprite(
        self, pixels: Pixels, pixel: tuple[int, int]
    ) -> None:
        """Draw a sprite's colored pixels in the middle of the cell."""
        px, py = pixel
        margin = (CELL_SIZE - SPRITE_SIZE) // 2
        self.renderer.put_pixels(pixels, px + margin, py + margin)

    def _draw_cell(
        self, cell: int, px: int, py: int
    ) -> None:
        """Draw the walls of one cell whose top-left pixel is (px, py)."""
        if cell == CLOSED_CELL:
            self.renderer.put_image(self._full_cell, px, py)
            return
        half = WALL_THICKNESS // 2
        if cell & NORTH:
            self.renderer.put_image(self._h_wall, px - half, py - half)
        if cell & SOUTH:
            self.renderer.put_image(
                self._h_wall, px - half, py + CELL_SIZE - half
            )
        if cell & WEST:
            self.renderer.put_image(self._v_wall, px - half, py - half)
        if cell & EAST:
            self.renderer.put_image(
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

    def _draw_hud(self, renderer: Renderer) -> None:
        """Draw the score, the lives, the level and the time left."""
        time_left = max(0, int(self.game.level_timer))
        texts = (
            f"Score: {self.game.score}",
            f"Lives: {self.game.lives}",
            f"Level: {self.game.current_level + 1}",
            f"Time: {time_left}",
        )
        column = renderer.width // len(texts)
        for index, text in enumerate(texts):
            x = HUD_MARGIN + index * column
            renderer.string_put(x, HUD_Y, HUD_COLOR, text)
