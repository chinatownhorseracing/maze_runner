from maze import create_maze, add_horizontal_wall, add_vertical_wall
from maze_runner import shortest_path
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
