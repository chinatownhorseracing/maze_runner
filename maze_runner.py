from maze import Maze, HorizontalWall, add_horizontal_wall, VerticalWall, get_dimensions
from runner import explore, create_maze, create_runner
from utils import render
from itertools import zip_longest
import argparse


def shortest_path(
    maze: Maze,
    starting: Optional[Tuple[int, int]] = None,
    goal: Optional[Tuple[int, int]] = None,
) -> List[Tuple[int, int, str]]:
    if starting is None:
        starting = (0, 0)
    if goal is None:
        goal = (maze.width - 1, maze.height - 1)

    runner = create_runner(starting[0], starting[1])
    runner_movements = explore(runner, maze)

    # Get all coordinates in path including duplicates
    runner_coordinates = [(x, y) for (x, y, actions) in runner_movements]

    # Here will be stored movements and coordinates already seen
    already_seen_movements = []
    already_seen_coordinates = []

    # Count all movements
    length = len(runner_movements)

    # For every position, action tuple in runner path
    for i in range(length):

        # If new coordinates add them to already seen list, also add the respective actions
        if runner_coordinates[i] not in already_seen_coordinates:
            already_seen_coordinates.append(runner_coordinates[i])
            already_seen_movements.append(runner_movements[i])
        else:
            # Used to delete everything from index of 1st repetition forward (the deadend path)
            index_1st_repetition = already_seen_coordinates.index(runner_coordinates[i])

            # Delete coordinates that led to dead end before returning to 2nd repetition of a coordinate
            # Also replace them with movement containing 2nd repetition of coordinates
            already_seen_coordinates[index_1st_repetition:] = []
            already_seen_coordinates.append(runner_coordinates[i])

            # Same as for coordinates but for the list containing both coordinates (positions) and actions
            already_seen_movements[index_1st_repetition:] = []
            already_seen_movements.append(runner_movements[i])

    # The already_seen_movements list was cleaned iteratively of dead ends now it's shortest path
    shortest_path = already_seen_movements
    return shortest_path


def maze_reader(maze_file: str) -> Maze:
    try:
        with open(maze_file, "r") as maze:
            lines = maze.read().splitlines()

            # Test maze contains just allowed symbols
            for line in lines:
                for char in line:
                    if char not in [".", "#"]:
                        raise ValueError("Not proper maze")

            # Reverse order of maze lines to make it easier to find hlines, vlines, xs, ys
            lines.reverse()

            """
            Find width of maze
            """
            # Ensure all lines have same length
            lengths_lines = [len(line) for line in lines]
            length_first_line = lengths_lines[0]
            line_lengths_equal = all(
                length == length_first_line for length in lengths_lines
            )
            if line_lengths_equal:
                length_line = length_first_line
                # Get maze width
                width = (length_line - 1) / 2
                if width.is_integer:
                    width = int(width)
            else:
                raise ValueError("Not proper maze")

            # If even number of columns instead of odd
            if length_line % 2 == 0:
                raise ValueError("Not proper maze")

            """
            Find maze height
            """
            # Since all lines have same length all columns have same number of elements (same height) so we check just 1
            number_lines = len(lines)
            height = (number_lines - 1) / 2
            if height.is_integer():
                height = int(height)
            else:
                raise ValueError("Not proper maze")

            # Now we can create blank maze of correct height and width
            maze = Maze(width, height)

            # Get hline numbers
            hlines = []
            for i in range(height + 1):
                hlines.append(i)

            # Get y's
            ys = []
            for i in range(height):
                ys.append(i)

            # Get vline numbers
            vlines = []
            for i in range(width + 1):
                vlines.append(i)

            # Get x's
            xs = []
            for i in range(width):
                xs.append(i)

            """
            Combine hlines and ys into a single vertical index list, 
            Same for vlines and ys into horizontal index list
            This will help index directly into maze figure given, adding walls at respective vertical, horizontal indexes
            After logic can be adjusted like if it's even index row add horizontal wall, if odd vertical wall
            """

            vertical_indexes = []
            # Iterate over hlines, y's interleaving into single list
            for hline, y in zip_longest(hlines, ys):
                vertical_indexes.append(hline)
                # Always 1 more hlines than ys need to remove null y
                if y is not None:
                    vertical_indexes.append(y)

            horizontal_indexes = []
            # Iterate over vlines, x's interleaving into single list
            for vline, x in zip_longest(vlines, xs):
                horizontal_indexes.append(vline)
                # Always 1 more vlines than xs need to remove null x
                if x is not None:
                    horizontal_indexes.append(x)

            """
            In this part we add the walls. There are 3 cases.
            Case 1 is row is first or last (counting from bottom up). Then we add horizontal walls for all x's,
            they are at horizontal indexes list from second every other element forward
            Case 2 is row has even index, then we add horizontal walls only where index of hash is odd in row
            (ignoring intersections between hlines and vlines, those are not walls)
            Case 3 is row has odd index, in this case we add vertical walls wherever is a hash
            """

            horizontal_walls = []
            vertical_walls = []
            for i in range(number_lines):
                # Case 1
                if i == 0 or i == number_lines - 1:
                    for j in range(1, length_line, 2):
                        horizontal_wall = HorizontalWall(
                            horizontal_indexes[j], vertical_indexes[i]
                        )
                        horizontal_walls.append(horizontal_wall)
                # Case 2
                elif i % 2 == 0:  # even row
                    # For odd indexes if there is hash there add horizontal wall
                    for j in range(1, length_line, 2):
                        if lines[i][j] == "#":
                            # print(f"vertical index {i}, horizontal index {j}")
                            # print(vertical_indexes[i], horizontal_indexes[j])
                            horizontal_wall = HorizontalWall(
                                horizontal_indexes[j], vertical_indexes[i]
                            )
                            horizontal_walls.append(horizontal_wall)
                # Case 3
                elif i % 2 != 0:  # odd row
                    # Vertical lines are between cells so first line then jumping over 1
                    for j in range(0, length_line, 2):
                        if lines[i][j] == "#":
                            # print(i, j)
                            vertical_wall = VerticalWall(
                                vertical_indexes[i], horizontal_indexes[j]
                            )
                            vertical_walls.append(vertical_wall)
            maze.horizontal_walls = horizontal_walls
            maze.vertical_walls = vertical_walls

            return maze

    except FileNotFoundError:
        raise IOError("Problem reading file")


# Used to convert string position typed by user into coordinates tuple
def parse_position(text: str) -> tuple[int, int]:
    coordinates = text.split(",")
    if len(coordinates) != 2:
        raise ValueError("Position must be in form x, y")
    x = int(coordinates[0])
    y = int(coordinates[1])
    return (x, y)


def write_statistics(
    maze_filename: str,
    exploration_steps: int,
    shortest_path: List[Tuple[int, int, str]],
) -> None:

    path_length = len(shortest_path)
    score = exploration_steps / 4 + path_length

    with open("statistics.txt", "w") as f:
        f.write(f"Input file name: {maze_filename}\n")
        f.write(f"Score: {score}\n")
        f.write(f"Number steps for exploration: {exploration_steps}\n")
        f.write(f"Shortest path found: {shortest_path}\n")
        f.write(f"Length shortest path found: {path_length}\n")


if __name__ == "__main__":

    # Add command line arguments for maze, start position, goal position
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    parser.add_argument("maze", help="The name of the maze file, e.g. maze1.mz")
    parser.add_argument(
        "--starting", help='The starting position, e.g. "2, 1"', default=None
    )
    parser.add_argument("--goal", help='The goal position, e.g. "4, 5"', default=None)
    args = parser.parse_args()

    # Try to read maze file handling any errors
    try:
        maze = maze_reader(args.maze)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    # Parse correct start, goal positions into tuple, handling any errors
    starting = None
    goal = None
    try:
        if args.starting is not None:
            starting = parse_position(args.starting)
        else:
            starting = (0, 0)
        if args.goal is not None:
            goal = parse_position(args.goal)
        else:
            goal = (maze.width - 1, maze.height - 1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

    width, height = get_dimensions(maze)

    # Validate if start, end positions within maze boundaries
    def validate_position(position):
        x, y = position
        return 0 <= x <= width - 1 and 0 <= y <= height - 1

    if starting is not None and not validate_position(starting):
        print("Error: starting position is outside the maze.")
        exit(1)
    if goal is not None and not validate_position(goal):
        print("Error: goal position is outside the maze.")
        exit(1)

    # Get statistics, handling any errors
    try:
        runner = create_runner(starting[0], starting[1])
        movements = explore(runner, maze, goal)
        steps = len(movements)
        path = shortest_path(maze, starting, goal)
        write_statistics(args.maze, steps, path)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)
