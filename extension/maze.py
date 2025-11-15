from collections import deque


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


def compute_flood_fill(maze: Maze, goal: Tuple[int, int]) -> List[List[int]]:

    width = maze.width
    height = maze.height

    # Make 2D list to store flood fill values
    values = []
    # For each row
    for i in range(height):
        row = []
        # For each element in row
        for j in range(width):
            row.append(None)
        values.append(row)

    # Set goal flood fill value to 0
    goal_x = goal[0]
    goal_y = goal[1]
    values[goal_y][goal_x] = 0

    # Initiate a queue
    queue = deque()
    queue.append((goal_x, goal_y))

    while queue:
        current_cell = queue.popleft()
        current_cell_x = current_cell[0]
        current_cell_y = current_cell[1]
        current_cell_value = values[current_cell_y][current_cell_x]

        # Get neighbors we can get to without being blocked by walls
        walls_around = get_walls(maze, current_cell_x, current_cell_y)
        reachable_neighbors = []
        # Add north cell if reachable
        if not walls_around[0]:
            reachable_neighbors.append((current_cell_x, current_cell_y + 1))
        # Add east cell if reachable
        if not walls_around[1]:
            reachable_neighbors.append((current_cell_x + 1, current_cell_y))
        # Add south cell if reachable
        if not walls_around[2]:
            reachable_neighbors.append((current_cell_x, current_cell_y - 1))
        # Add west cell if reachable
        if not walls_around[3]:
            reachable_neighbors.append((current_cell_x - 1, current_cell_y))

        # Update neighbor values and queue them to get their neighbors also
        for neighbor in reachable_neighbors:
            neighbor_x = neighbor[0]
            neighbor_y = neighbor[1]
            if 0 <= neighbor_x < width and 0 <= neighbor_y < height:
                if values[neighbor_y][neighbor_x] is None:
                    values[neighbor_y][neighbor_x] = current_cell_value + 1
                    queue.append(neighbor)
    return values
