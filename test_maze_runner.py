from maze import create_maze, add_horizontal_wall, add_vertical_wall
from maze_runner import shortest_path


# def test_shortest_path() -> None:
#     """A Unit test for :py:func:`~maze_runner.shortest_path`

#     Below is the test sequence:

#     1. Create a maze of size (11, 5).

#     2. Add a horizontal wall at (0, 1).

#     3. Add a vertical wall at (1, 1).

#     4. Run short_path function to get the path (with default start and goal).

#     5. Check that the result is a valid path, starting from (0,0) and end at
#        (10, 4).
#     """
#     maze = create_maze(11, 5)
#     maze = add_horizontal_wall(maze, 0, 1)
#     maze = add_vertical_wall(maze, 1, 1)
#     path = shortest_path(maze)
#     assert path[0] == (0, 0, "RF")
#     assert path[-1] == (9, 4, "F")
#     prefix = []
#     for location in path:
#         x, y, a = location
#         assert (x, y) not in prefix, f"{location} is repeated"
#         prefix.append((x, y))
