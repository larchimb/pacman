import random
from typing import Any
from mlx import Mlx
from mazegenerator import MazeGenerator


class DisplayMaze:
    """Class for diplay the maze with mlx"""

    def __init__(self, maze: MazeGenerator) -> None:
        """Initiliaze the maze's values, and defaults colors"""
        self.maze_gen: MazeGenerator = maze
        self.initialize_maze_settings()
        self.wall_color: tuple[int, int, int, int] = (255, 255, 255, 220)
        self.path_color: tuple[int, int, int, int] = (100, 150, 110, 255)
        self.entry_color: tuple[int, int, int, int] = (0, 215, 0, 200)
        self.exit_color: tuple[int, int, int, int] = (0, 0, 215, 200)

        self.wall_size: float = 0.2
        self.wdw_percent: float = 0.4
        self.h_menu: int = 25
        self.printable: bool = True

    def initialize_maze_settings(self) -> None:
        """Initialize maze's settings from the maze generator"""
        self.cells: list[list[int]] = self.maze_gen.maze
        self.rows: int = len(self.cells)
        self.column: int = len(self.cells[0])
        self.entry: tuple[int, int] = self.maze_gen.maze_entry
        self.exit: tuple[int, int] = self.maze_gen.maze_exit
        path: str | bool = self.maze_gen.shortest_path
        if not isinstance(path, str) or not path:
            raise Exception("There is no solution path in the maze")
        self.path: str = path

        self.path_visible: bool = False

    def initialize_display_settings(self) -> None:
        """Initialize mlx and window's settings"""
        self.m: Mlx = Mlx()
        self.mlx_ptr: Any = self.m.mlx_init()
        self.calculate_img_values()

        try:
            if not self.printable:
                raise Exception(
                    "The maze can't be displayed, not readable or too big"
                    )
            self.win_ptr: Any = self.m.mlx_new_window(
                self.mlx_ptr, self.w_wdw, self.h_wdw, "A_Maze_zing"
            )
            self.img: Any = self.m.mlx_new_image(
                self.mlx_ptr,
                self.w_img,
                self.h_img
                )
            self.data: Any
            self.bit_per_pixel: Any
            self.size_line: Any
            the_format: Any
            self.data, self.bit_per_pixel, self.size_line, the_format = (
                self.m.mlx_get_data_addr(self.img)
            )
            self.menu_settings()
            self.regenerate: bool
            self.draw()
        except Exception as e:
            print(e)

    def calculate_img_values(self) -> None:
        """Calculate the value of a cell and of a wall in pixel"""
        ret: Any
        self.w: int
        self.h: int
        ret, self.w, self.h = self.m.mlx_get_screen_size(self.mlx_ptr)
        self.cell_size: int = 0
        self.wall: int = 0
        wdw_size: float = self.wdw_percent

        while self.cell_size < 5 or self.wall < 2:
            self.w_wdw: int = int(self.w * wdw_size)
            self.h_wdw: int = int(self.h * wdw_size)

            w_cell: int = int(
                self.w_wdw /
                (self.column + ((self.column + 1) * self.wall_size))
            )
            h_cell: int = int(
                (self.h_wdw - self.h_menu) /
                (self.rows + ((self.rows + 1) * self.wall_size))
            )

            if w_cell > h_cell:
                self.cell_size = h_cell
            else:
                self.cell_size = w_cell

            self.wall = int(self.cell_size * self.wall_size)
            wdw_size += 0.05

        if (wdw_size > 1):
            self.printable = False

        self.w_img: int = self.column * (
                self.cell_size + self.wall) + self.wall
        self.h_img: int = self.rows * (
                self.cell_size + self.wall) + self.wall
        self.w_wdw = self.w_img + 20
        self.h_wdw = self.h_img + 20 + self.h_menu
        if self.w_wdw > int(self.w * wdw_size):
            self.w_wdw = int(self.w * wdw_size)
        if self.h_wdw > int(self.h * wdw_size):
            self.h_wdw = int(self.h * wdw_size)
        self.w_offset: int = int((self.w_wdw - self.w_img) / 2)
        self.h_offset: int = int((self.h_wdw - self.h_menu - self.h_img) / 2)

    def menu_settings(self) -> None:
        """Create and print the menu in the window"""
        single_char: int = 6
        h_menu: int = self.h_wdw - self.h_menu
        color: int = 0xFFFFFF
        options: list[str] = [
            "1: Regenerate",
            "2: Path",
            "3: Wall color",
            "4: Exit"
            ]
        space_menu: int = int(
            (self.w_wdw -
             (single_char * sum([len(element) for element in options]))) /
            (len(options) + 1)
        )
        i: int
        position: int
        for i in range(0, len(options)):
            if not i == 0:
                position = (i + 1) * space_menu + single_char * sum(
                    [len(element) for element in options[:i]]
                )
            else:
                position = space_menu
            self.m.mlx_string_put(
                self.mlx_ptr, self.win_ptr, position, h_menu, color, options[i]
            )

    def gere_close(self, _: Any) -> None:
        """For closing the window"""
        self.m.mlx_loop_exit(self.mlx_ptr)

    def draw_walls(self, color: tuple[int, int, int, int]) -> None:
        """Draw the walls of the maze"""
        x: int
        y: int
        i: int
        j: int
        k: int
        cell: int
        offset: int
        for x in range(0, self.column):
            for y in range(0, self.rows):
                cell = self.cells[y][x]
                if cell & 1 == 1:
                    for i in range(0, self.cell_size + 2 * self.wall):
                        for j in range(0, self.wall):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if cell & 8 == 8:
                    for i in range(0, self.wall):
                        for j in range(0, self.cell_size + self.wall * 2):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if x == self.column - 1:
                    for i in range(
                        self.cell_size + self.wall,
                        self.cell_size + (self.wall * 2)
                    ):
                        for j in range(0, self.wall + self.cell_size):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

                if y == self.rows - 1:
                    for i in range(0, self.cell_size + 2 * self.wall):
                        for j in range(
                            self.cell_size + self.wall,
                            self.cell_size + (2 * self.wall)
                        ):
                            offset = (
                                (x * (self.cell_size + self.wall) + i) *
                                (self.bit_per_pixel // 8) +
                                (y * (self.cell_size + self.wall) + j) *
                                self.size_line
                                      )
                            for k in range(0, 4):
                                self.data[offset + k] = color[k]

    def color_extremities_case(
                    self,
                    x: int,
                    y: int,
                    color: tuple[int, int, int, int]) -> None:
        """Color the inside of a cell"""
        i: int
        j: int
        k: int
        offset: int
        for i in range(self.wall, self.cell_size + self.wall):
            for j in range(self.wall, self.cell_size + self.wall):
                offset = (
                    (x * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8) +
                    (y * (self.cell_size + self.wall) + j) * self.size_line
                )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]

    def color_a_case(self,
                     x: int,
                     y: int,
                     direction: str,
                     color: tuple[int, int, int, int]) -> None:
        """Color the inside of a cell"""
        i_start: int = 0
        i_end: int = 0
        j_start: int = 0
        j_end: int = 0
        if direction == 'N':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = self.wall * 2
            j_end = self.cell_size + self.wall * 3

        elif direction == 'E':
            i_start = -self.wall
            i_end = self.cell_size
            j_start = self.wall * 2
            j_end = self.cell_size

        elif direction == 'S':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = -self.wall
            j_end = self.cell_size

        elif direction == 'W':
            i_start = self.wall * 2
            i_end = self.cell_size + self.wall * 3
            j_start = self.wall * 2
            j_end = self.cell_size

        i: int
        j: int
        k: int
        offset: int
        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                offset = (
                    (x * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8) +
                    (y * (self.cell_size + self.wall) + j) * self.size_line
                )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]
        self.display(None)

    def one_direction_path(
                    self,
                    x: int,
                    y: int,
                    direction: str,
                    color: tuple[int, int, int, int]) -> None:
        """ draw the path on a normal situation """
        i_start: int = 0
        i_end: int = 0
        j_start: int = 0
        j_end: int = 0
        if direction == 'N':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = self.cell_size + self.wall
            j_end = self.cell_size + self.wall * 2
            y -= 1

        elif direction == 'E':
            i_start = 0
            i_end = self.wall
            j_start = self.wall * 2
            j_end = self.cell_size
            x += 1

        elif direction == 'S':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = 0
            j_end = self.wall
            y += 1

        elif direction == 'W':
            i_start = self.cell_size + self.wall
            i_end = self.cell_size + self.wall * 2
            j_start = self.wall * 2
            j_end = self.cell_size
            x -= 1

        i: int
        j: int
        k: int
        offset: int
        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                offset = (
                    (x * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8) +
                    (y * (self.cell_size + self.wall) + j) * self.size_line
                )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]
        self.display(None)

    def color_first_path_case(
                    self,
                    x: int,
                    y: int,
                    direction: str,
                    color: tuple[int, int, int, int]) -> tuple[int, int]:
        """ draw the path on the fist case """
        i_start: int = 0
        i_end: int = 0
        j_start: int = 0
        j_end: int = 0
        if direction == 'N':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = self.wall * 2
            j_end = self.cell_size + self.wall * 2
            y -= 1

        elif direction == 'E':
            i_start = 0
            i_end = self.cell_size
            j_start = self.wall * 2
            j_end = self.cell_size
            x += 1

        elif direction == 'S':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = 0
            j_end = self.cell_size
            y += 1

        elif direction == 'W':
            i_start = self.wall * 2
            i_end = self.cell_size + self.wall * 2
            j_start = self.wall * 2
            j_end = self.cell_size
            x -= 1

        i: int
        j: int
        k: int
        offset: int
        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                offset = (
                    (x * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8) +
                    (y * (self.cell_size + self.wall) + j) * self.size_line
                )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]
        self.display(None)
        return (x, y)

    def color_last_path_case(
                    self,
                    x: int,
                    y: int,
                    direction: str,
                    color: tuple[int, int, int, int]) -> None:
        """ draw the path on the last case """
        i_start: int = 0
        i_end: int = 0
        j_start: int = 0
        j_end: int = 0
        if direction == 'N':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = self.cell_size + self.wall
            j_end = self.cell_size + self.wall * 3
            y -= 1

        elif direction == 'E':
            i_start = -self.wall
            i_end = self.wall
            j_start = self.wall * 2
            j_end = self.cell_size
            x += 1

        elif direction == 'S':
            i_start = self.wall * 2
            i_end = self.cell_size
            j_start = -self.wall
            j_end = self.wall
            y += 1

        elif direction == 'W':
            i_start = self.cell_size + self.wall
            i_end = self.cell_size + self.wall * 3 + 1
            j_start = self.wall * 2
            j_end = self.cell_size
            x -= 1

        i: int
        j: int
        k: int
        offset: int
        for i in range(i_start, i_end):
            for j in range(j_start, j_end):
                offset = (
                    (x * (self.cell_size + self.wall) + i) *
                    (self.bit_per_pixel // 8) +
                    (y * (self.cell_size + self.wall) + j) * self.size_line
                )
                for k in range(0, 4):
                    self.data[offset + k] = color[k]
        self.display(None)

    def draw_forty_two(self, color: tuple[int, int, int, int]) -> None:
        """Fill the forty-two symbol's cells (fully closed cells)"""
        x: int
        y: int
        for y in range(0, self.rows):
            for x in range(0, self.column):
                if self.cells[y][x] == 15:
                    self.color_extremities_case(x, y, color)

    def draw_the_path(self, color: tuple[int, int, int, int]) -> None:
        """Draw or undraw the path between the entry to the exit"""
        x: int = self.entry[0]
        y: int = self.entry[1]

        if self.path_visible:
            color = (0, 0, 0, 255)
            self.path_visible = False
        else:
            self.path_visible = True

        if len(self.path) == 1:
            self.one_direction_path(x, y, self.path[0], color)
            return

        x, y = self.color_first_path_case(x, y, self.path[0], color)

        i: str
        for i in self.path[1:-1]:
            if i == "N":
                self.color_a_case(x, y - 1, 'N', color)
                y -= 1
            elif i == "E":
                self.color_a_case(x + 1, y, 'E', color)
                x += 1
            elif i == "S":
                self.color_a_case(x, y + 1, 'S', color)
                y += 1
            elif i == "W":
                self.color_a_case(x - 1, y, 'W', color)
                x -= 1

        self.color_last_path_case(x, y, self.path[-1], color)

    def clean_image(self) -> None:
        """Reinitialize the image to a black backscreen"""
        color: tuple[int, int, int, int] = (0, 0, 0, 255)
        x: int
        y: int
        k: int
        offset: int
        for x in range(self.h_img):
            for y in range(self.w_img):
                offset = x * self.size_line + y * (self.bit_per_pixel // 8)
                for k in range(0, 4):
                    self.data[offset + k] = color[k]

    def mymouse(self, button: int, x: int, y: int, mystuff: Any) -> None:
        """Manage operations related to mouse click in the window"""
        pass

    def mykey(self, keynum: int, mystuff: Any) -> None:
        """Manages some operations related to key activation"""

        if keynum == 32:
            self.m.mlx_mouse_hook(self.win_ptr, None, None)

        elif keynum == 65307 or keynum == 52 or keynum == 65430:
            self.m.mlx_loop_exit(self.mlx_ptr)

        elif keynum == 49 or keynum == 65436:
            self.regenerate = True
            self.m.mlx_loop_exit(self.mlx_ptr)

        elif keynum == 50 or keynum == 65433:
            self.draw_the_path(self.path_color)

        elif keynum == 51 or keynum == 65435:
            self.wall_color = (
                random.randint(0, 255),
                random.randint(0, 255),
                random.randint(0, 255),
                255,
            )
            if self.path_visible:
                self.path_visible = False
            else:
                self.path_visible = True
            self.draw_walls(self.wall_color)
            self.draw_forty_two(self.wall_color)
            self.display(None)

    def display(self, _: Any) -> None:
        """Display the image in the window"""
        self.m.mlx_put_image_to_window(
            self.mlx_ptr, self.win_ptr, self.img, self.w_offset, self.h_offset
        )
        self.m.mlx_sync(self.mlx_ptr, 2, self.win_ptr)

    def draw(self) -> None:
        """Draw in image's buffer"""
        self.regenerate = False
        self.clean_image()
        self.draw_walls(self.wall_color)
        self.draw_forty_two(self.wall_color)
        self.color_extremities_case(
            self.entry[0], self.entry[1], self.entry_color
            )
        self.color_extremities_case(
            self.exit[0], self.exit[1], self.exit_color
            )
        self.draw_the_path(self.path_color)

        self.m.mlx_mouse_hook(self.win_ptr, self.mymouse, None)
        self.m.mlx_key_hook(self.win_ptr, self.mykey, None)
        self.m.mlx_hook(self.win_ptr, 33, 0, self.gere_close, None)
        self.display(None)

        self.m.mlx_loop(self.mlx_ptr)

        if self.regenerate:
            self.m.mlx_destroy_image(self.mlx_ptr, self.img)
            self.img = self.m.mlx_new_image(
                self.mlx_ptr, self.w_img, self.h_img
                )
            self.data, self.bit_per_pixel, self.size_line, the_format = (
                self.m.mlx_get_data_addr(self.img)
            )
            self.maze_gen.generate()
            self.initialize_maze_settings()
            self.draw()
            return

        self.m.mlx_destroy_image(self.mlx_ptr, self.img)
        self.m.mlx_destroy_window(self.mlx_ptr, self.win_ptr)
        self.m.mlx_release(self.mlx_ptr)
