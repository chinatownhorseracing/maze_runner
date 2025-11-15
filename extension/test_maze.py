from maze import (
    HorizontalWall,
    VerticalWall,
    create_maze,
    Maze,
    add_horizontal_wall,
    add_vertical_wall,
    get_dimensions,
    get_walls,
)
from runner import create_runner


def test_horizontal_wall():

    # Test horizontal wall created properly
    wall = HorizontalWall(1, 2)
    assert isinstance(wall, HorizontalWall)
    assert wall.x == 1
    assert wall.hline == 2

    # Test equality working well
    wall1 = HorizontalWall(1, 2)
    wall2 = HorizontalWall(1, 2)
    assert wall1 == wall2


def test_vertical_wall():

    # Test vertical wall created properly
    wall = VerticalWall(1, 2)
    assert isinstance(wall, VerticalWall)
    assert wall.y == 1
    assert wall.vline == 2

    # Test equality working well
    wall1 = VerticalWall(1, 2)
    wall2 = VerticalWall(1, 2)
    assert wall1 == wall2


def test_create_maze():

    # Test default maze creation
    maze = create_maze()
    assert isinstance(maze, Maze)
    assert maze.width == 5
    assert maze.height == 5

    # Test maze creation
    maze = create_maze(1, 2)
    assert isinstance(maze, Maze)
    assert maze.width == 1
    assert maze.height == 2


def test_external_horizontal_walls():

    # Test horizontal external walls maze odd width even height
    maze = create_maze(1, 2)
    horizontal_walls = maze.horizontal_walls
    for wall in horizontal_walls:
        print(f"Horizontal wall at x-coordinate {wall.x}, hline {wall.hline}")
    horizontal_walls_x_coordinates = [wall.x for wall in horizontal_walls]
    horizontal_walls_hlines = [wall.hline for wall in horizontal_walls]
    assert horizontal_walls_x_coordinates == [0, 0]
    assert horizontal_walls_hlines == [0, 2]

    # Test horizontal external walls maze even width odd height
    maze = create_maze(2, 1)
    horizontal_walls = maze.horizontal_walls
    for wall in horizontal_walls:
        print(f"Horizontal wall at x-coordinate {wall.x}, hline {wall.hline}")
    horizontal_walls_x_coordinates = [wall.x for wall in horizontal_walls]
    horizontal_walls_hlines = [wall.hline for wall in horizontal_walls]
    assert horizontal_walls_x_coordinates == [0, 1, 0, 1]
    assert horizontal_walls_hlines == [0, 0, 1, 1]

    # Test horizontal external walls maze even width even height
    maze = create_maze(2, 2)
    horizontal_walls = maze.horizontal_walls
    for wall in horizontal_walls:
        print(f"Horizontal wall at x-coordinate {wall.x}, hline {wall.hline}")
    horizontal_walls_x_coordinates = [wall.x for wall in horizontal_walls]
    horizontal_walls_hlines = [wall.hline for wall in horizontal_walls]
    assert horizontal_walls_x_coordinates == [0, 1, 0, 1]
    assert horizontal_walls_hlines == [0, 0, 2, 2]

    # Test horizontal external walls maze odd width odd height
    maze = create_maze(1, 1)
    horizontal_walls = maze.horizontal_walls
    for wall in horizontal_walls:
        print(f"Horizontal wall at x-coordinate {wall.x}, hline {wall.hline}")
    horizontal_walls_x_coordinates = [wall.x for wall in horizontal_walls]
    horizontal_walls_hlines = [wall.hline for wall in horizontal_walls]
    assert horizontal_walls_x_coordinates == [0, 0]
    assert horizontal_walls_hlines == [0, 1]


def test_external_vertical_walls():

    # Test vertical external walls maze odd width even height
    maze = create_maze(1, 2)
    vertical_walls = maze.vertical_walls
    for wall in vertical_walls:
        print(f"Vertical wall at y-coordinate {wall.y}, vline {wall.vline}")
    vertical_walls_y_coordinates = [wall.y for wall in vertical_walls]
    vertical_walls_vlines = [wall.vline for wall in vertical_walls]
    assert vertical_walls_y_coordinates == [0, 1, 0, 1]
    assert vertical_walls_vlines == [0, 0, 1, 1]

    # Test vertical external walls maze even width odd height
    maze = create_maze(2, 1)
    vertical_walls = maze.vertical_walls
    for wall in vertical_walls:
        print(f"Vertical wall at y-coordinate {wall.y}, vline {wall.vline}")
    vertical_walls_y_coordinates = [wall.y for wall in vertical_walls]
    vertical_walls_vlines = [wall.vline for wall in vertical_walls]
    assert vertical_walls_y_coordinates == [0, 0]
    assert vertical_walls_vlines == [0, 2]

    # Test vertical external walls maze even width even height
    maze = create_maze(2, 2)
    vertical_walls = maze.vertical_walls
    for wall in vertical_walls:
        print(f"Vertical wall at y-coordinate {wall.y}, vline {wall.vline}")
    vertical_walls_y_coordinates = [wall.y for wall in vertical_walls]
    vertical_walls_vlines = [wall.vline for wall in vertical_walls]
    assert vertical_walls_y_coordinates == [0, 1, 0, 1]
    assert vertical_walls_vlines == [0, 0, 2, 2]

    # Test vertical external walls maze odd width odd height
    maze = create_maze(1, 1)
    vertical_walls = maze.vertical_walls
    for wall in vertical_walls:
        print(f"Vertical wall at y-coordinate {wall.y}, vline {wall.vline}")
    vertical_walls_y_coordinates = [wall.y for wall in vertical_walls]
    vertical_walls_vlines = [wall.vline for wall in vertical_walls]
    assert vertical_walls_y_coordinates == [0, 0]
    assert vertical_walls_vlines == [0, 1]


def test_add_horizontal_wall():
    maze = create_maze(11, 5)
    horizontal_walls = maze.horizontal_walls
    horizontal_walls.append(HorizontalWall(5, 2))

    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 5, 2)
    horizontal_walls_new = maze.horizontal_walls

    assert horizontal_walls == horizontal_walls_new


def test_add_vertical_wall():

    maze = create_maze(11, 5)
    vertical_walls = maze.vertical_walls
    vertical_walls.append(VerticalWall(2, 4))

    maze = create_maze(11, 5)
    maze = add_vertical_wall(maze, 2, 4)
    vertical_walls_new = maze.vertical_walls

    assert vertical_walls == vertical_walls_new


def test_get_dimensions():
    maze = create_maze()
    dimensions = get_dimensions(maze)
    assert dimensions == (5, 5)


def test_get_walls():

    # Maze shown in figure used for all tests
    maze = create_maze(11, 5)

    # Test if showing no random internal walls that shouldn't be there
    assert get_walls(maze, 4, 2) == (False, False, False, False)

    # Test if detects wall above
    assert get_walls(maze, 5, 4) == (True, False, False, False)

    # Test if detects wall below
    assert get_walls(maze, 5, 0) == (False, False, True, False)

    # Test if detects wall left
    assert get_walls(maze, 0, 3) == (False, False, False, True)

    # Test if detects wall right
    assert get_walls(maze, 10, 2) == (False, True, False, False)

    # Test if detects more than 1 wall
    assert get_walls(maze, 0, 0) == (False, False, True, True)
