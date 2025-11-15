class HorizontalWall:
    def __init__(self, x: int, hline: int):
        self.x = x
        self.hline = hline

    # When checking if 2 horizontal walls are the same check by value not memory address
    def __eq__(self, other_wall):
        return (
            isinstance(other_wall, HorizontalWall)
            and self.x == other_wall.x
            and self.hline == other_wall.hline
        )


class VerticalWall:
    def __init__(self, y: int, vline: int):
        self.y = y
        self.vline = vline

    # When checking if 2 vertical walls are the same check by value not memory address
    def __eq__(self, other_wall):
        return (
            isinstance(other_wall, VerticalWall)
            and self.y == other_wall.y
            and self.vline == other_wall.vline
        )


class Maze:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.horizontal_walls = []
        self.vertical_walls = []


# Put horizontal, vertical walls around the maze
def create_maze(width: int = 5, height: int = 5) -> Maze:
    maze = Maze(width, height)

    # Lists to store external walls
    horizontal_walls = []
    vertical_walls = []

    # Add horizontal walls from below (starting hline)
    hline = 0
    for i in range(width):
        horizontal_wall = HorizontalWall(i, hline)
        horizontal_walls.append(horizontal_wall)

    # Add horizontal walls from above (last hline)
    hline = height
    for i in range(width):
        horizontal_wall = HorizontalWall(i, hline)
        horizontal_walls.append(horizontal_wall)

    # Add left vertical walls (starting vline)
    vline = 0
    for i in range(height):
        vertical_wall = VerticalWall(i, vline)
        vertical_walls.append(vertical_wall)

    # Add right vertical walls (last vline)
    vline = width
    for i in range(height):
        vertical_wall = VerticalWall(i, vline)
        vertical_walls.append(vertical_wall)

    # Add external walls to maze object
    maze.horizontal_walls = horizontal_walls
    maze.vertical_walls = vertical_walls

    return maze


def add_horizontal_wall(maze: Maze, x_coordinate: int, horizontal_line: int) -> Maze:
    horizontal_wall = HorizontalWall(x_coordinate, horizontal_line)

    # Add new wall to maze's horizontal walls list
    maze.horizontal_walls.append(horizontal_wall)

    return maze


def add_vertical_wall(maze: Maze, y_coordinate: int, vertical_line: int) -> Maze:
    vertical_wall = VerticalWall(y_coordinate, vertical_line)

    # Add new wall to maze's vertical walls list
    maze.vertical_walls.append(vertical_wall)

    return maze


def get_dimensions(maze: Maze) -> Tuple[int, int]:
    width = maze.width
    height = maze.height
    dimensions = (width, height)
    return dimensions


def get_walls(
    maze: Maze, x_coordinate: int, y_coordinate: int
) -> Tuple[bool, bool, bool, bool]:
    # Based on cell at (4,2) from figure find vlines, hlines and x,y coord of potential neighbouring walls
    potential_north_neighbour = HorizontalWall(x=x_coordinate, hline=y_coordinate + 1)
    potential_east_neighbour = VerticalWall(y=y_coordinate, vline=x_coordinate + 1)
    potential_south_neighbour = HorizontalWall(x=x_coordinate, hline=y_coordinate)
    potential_west_neighbour = VerticalWall(y=y_coordinate, vline=x_coordinate)

    # Add potential neighbours to a list to iteratively check each of them against maze walls
    present_horizontal_walls = maze.horizontal_walls
    present_vertical_walls = maze.vertical_walls

    # Check if at potential neighbour coordinates there actually is a wall
    n = e = s = w = False
    if potential_north_neighbour in present_horizontal_walls:
        n = True
    if potential_east_neighbour in present_vertical_walls:
        e = True
    if potential_south_neighbour in present_horizontal_walls:
        s = True
    if potential_west_neighbour in present_vertical_walls:
        w = True

    walls_around = (n, e, s, w)
    return walls_around
