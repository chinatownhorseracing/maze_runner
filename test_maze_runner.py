import pytest
from maze import (
    create_maze,
    add_horizontal_wall,
    add_vertical_wall,
    HorizontalWall,
    get_dimensions,
)
from maze_runner import shortest_path, maze_reader
from runner import create_runner, explore


def test_shortest_path():

    # Test from test harness on gitlab used
    maze = create_maze(11, 5)
    maze = add_horizontal_wall(maze, 0, 1)
    maze = add_vertical_wall(maze, 1, 1)
    path = shortest_path(maze)
    assert path[0] == (0, 0, "RF")
    assert path[-1] == (9, 4, "F")
    prefix = []
    for location in path:
        x, y, a = location
        assert (x, y) not in prefix, f"{location} is repeated"
        prefix.append((x, y))


def test_maze_reader():

    # Test walls added manually are same as through maze reader
    maze1 = create_maze(9, 5)
    maze1.horizontal_walls.insert(9, HorizontalWall(4, 2))

    maze2 = maze_reader("mazes/maze.txt")
    maze1_horizontal_walls = maze1.horizontal_walls
    maze2_horizontal_walls = maze2.horizontal_walls

    assert maze1_horizontal_walls == maze2_horizontal_walls

    # Test error when problem reading file
    with pytest.raises(IOError):
        maze = maze_reader("Notexist.txt")

    # Test maze dimensions correct
    maze = maze_reader("mazes/maze.txt")
    assert get_dimensions(maze) == (9, 5)

    # Test error when file rows don't have same number of elements
    with pytest.raises(ValueError):
        maze = maze_reader("mazes/bad_maze.txt")

    # Test error for even number of columns
    with pytest.raises(ValueError):
        maze = maze_reader("mazes/bad_maze2.txt")

    # Test error for even number of rows
    with pytest.raises(ValueError):
        maze = maze_reader("mazes/bad_maze3.txt")

    # Test error when maze has symbol that is not dot or hash
    with pytest.raises(ValueError):
        maze = maze_reader("mazes/bad_maze4.txt")
