from maze import create_maze, get_dimensions, get_walls
from runner import create_runner, get_x, get_y, get_orientation


def render(maze, runner=None) -> str:

    width, height = get_dimensions(maze)

    # make a grid of . characters
    char_width = 1 + 2 * width
    char_height = 1 + 2 * height
    chars = [["."] * char_width for _ in range(0, char_height)]

    # fill in the points on the grid that
    for char_y in range(0, char_height, 2):
        for char_x in range(0, char_width, 2):
            chars[char_y][char_x] = "#"

    # for all positions in the maze
    for y_coord in range(0, height):
        for x_coord in range(0, width):
            n, e, s, w = get_walls(maze, x_coord, y_coord)

            char_x = 1 + 2 * x_coord
            char_y = 1 + 2 * y_coord

            if n:
                chars[char_y + 1][char_x] = "#"
            if e:
                chars[char_y][char_x + 1] = "#"
            if s:
                chars[char_y - 1][char_x] = "#"
            if w:
                chars[char_y][char_x - 1] = "#"

    if runner:
        x_coord, y_coord = (
            get_x(runner),
            get_y(runner),
        )
        char_x = 1 + 2 * x_coord
        char_y = 1 + 2 * y_coord
        orientation = get_orientation(runner)
        chars[char_y][char_x] = {"N": "^", "E": ">", "S": "v", "W": "<"}[orientation]

    return "\n".join(["".join(r) for r in reversed(chars)])
