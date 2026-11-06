"""Big pixel letters for titles, built block by block like MLX images."""

from src.graphical.renderer import Image, Renderer

LETTER_HEIGHT: int = 5

PIXEL_FONT: dict[str, tuple[str, ...]] = {
    "A": (".###.", "#...#", "#####", "#...#", "#...#"),
    "C": (".####", "#....", "#....", "#....", ".####"),
    "E": ("#####", "#....", "####.", "#....", "#####"),
    "G": (".####", "#....", "#..##", "#...#", ".###."),
    "I": ("###", ".#.", ".#.", ".#.", "###"),
    "M": ("#...#", "##.##", "#.#.#", "#...#", "#...#"),
    "N": ("#...#", "##..#", "#.#.#", "#..##", "#...#"),
    "O": (".###.", "#...#", "#...#", "#...#", ".###."),
    "P": ("####.", "#...#", "####.", "#....", "#...."),
    "R": ("####.", "#...#", "####.", "#..#.", "#...#"),
    "S": (".####", "#....", ".###.", "....#", "####."),
    "T": ("#####", "..#..", "..#..", "..#..", "..#.."),
    "U": ("#...#", "#...#", "#...#", "#...#", ".###."),
    "V": ("#...#", "#...#", "#...#", ".#.#.", "..#.."),
    "Y": ("#...#", ".#.#.", "..#..", "..#..", "..#.."),
    "-": ("...", "...", "###", "...", "..."),
    " ": ("...", "...", "...", "...", "..."),
}


def pixel_rows(text: str) -> list[str]:
    """Return the rows of a big text, one empty column between letters."""
    letters = [PIXEL_FONT.get(char, PIXEL_FONT[" "]) for char in text.upper()]
    return [
        ".".join(letter[row] for letter in letters)
        for row in range(LETTER_HEIGHT)
    ]


def new_pixel_image(
    renderer: Renderer, rows: list[str], color: int, block: int
) -> Image:
    """Create an image where each '#' of rows is a block x block square."""
    image = renderer.new_image(len(rows[0]) * block, len(rows) * block)
    for row, line in enumerate(rows):
        for col, char in enumerate(line):
            if char != "#":
                continue
            for y in range(block):
                for x in range(block):
                    renderer.image_pixel_put(
                        image, col * block + x, row * block + y, color
                    )
    return image
