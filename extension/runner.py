# Import maze object and its function to help implement sense_walls for runner
from maze import Maze, get_walls, create_maze
import csv
from maze import compute_flood_fill


class Runner:
    def __init__(self, x: int, y: int, orientation: str):
        self.x = x
        self.y = y
        self.orientation = orientation


def create_runner(x: int = 0, y: int = 0, orientation: str = "N") -> Runner:
    return Runner(x, y, orientation)


def get_x(runner: Runner) -> int:
    return runner.x


def get_y(runner: Runner) -> int:
    return runner.y


def get_orientation(runner: Runner) -> str:
    return runner.orientation


def turn(runner: Runner, direction: str) -> Runner:

    # List represents a circle for moving left and right between orientations
    orientations = ["N", "E", "S", "W"]

    runner_orientation = get_orientation(runner)

    # Get circle index for runner orientation
    circle_index = 0
    for i in range(len(orientations)):
        if orientations[i] == runner_orientation:
            circle_index = i

    # Convert direction to index move -1 for left +1 for right in orientations list
    move = 0
    if direction == "Left":
        move -= 1
    elif direction == "Right":
        move += 1

    # Move left/right in list representing circle, wraparound if exceed last index
    new_circle_index = (circle_index + move) % len(orientations)

    # Change runner orientation
    new_orientation = orientations[new_circle_index]
    runner.orientation = new_orientation
    return runner


def forward(runner: Runner) -> Runner:

    # Get current data on the runner
    runner_orientation = get_orientation(runner)
    runner_x = get_x(runner)
    runner_y = get_y(runner)

    # Change x,y coordinates dependinding on orientation
    if runner_orientation == "N":
        runner_y += 1
    elif runner_orientation == "S":
        runner_y -= 1
    elif runner_orientation == "W":
        runner_x -= 1
    elif runner_orientation == "E":
        runner_x += 1

    # Set runner object's new coordinates to changed ones
    runner.x = runner_x
    runner.y = runner_y

    return runner


def sense_walls(runner: Runner, maze: Maze) -> Tuple[bool, bool, bool]:

    # Check North, East, South, West directions around cell to see which has walls
    n, e, s, w = get_walls(maze, runner.x, runner.y)

    # Map direction keys to booleans showing if there is wall there
    direction_walls = {}
    direction_walls["N"] = n
    direction_walls["E"] = e
    direction_walls["S"] = s
    direction_walls["W"] = w

    runner_orientation = get_orientation(runner)

    # Find left, front, right depending on runner orientation
    if runner_orientation == "N":
        left = "W"
        front = "N"
        right = "E"
    elif runner_orientation == "E":
        left = "N"
        front = "E"
        right = "S"
    elif runner_orientation == "S":
        left = "E"
        front = "S"
        right = "W"
    elif runner_orientation == "W":
        left = "S"
        front = "W"
        right = "N"

    # Get boolean values from direction dictionary at left, front, right of player
    has_left_wall = direction_walls[left]
    has_front_wall = direction_walls[front]
    has_right_wall = direction_walls[right]

    walls_around_runner = (has_left_wall, has_front_wall, has_right_wall)
    return walls_around_runner


def go_straight(runner: Runner, maze: Maze) -> Runner:

    walls_around_runner = sense_walls(runner, maze)

    # Get second boolean value for wall in front
    has_wall_ahead = walls_around_runner[1]

    if has_wall_ahead:
        raise ValueError("There is a wall in front")

    runner = forward(runner)
    return runner


def move(runner: Runner, maze: Maze, values: List[List[int]]) -> Tuple[Runner, str]:

    runner_x = runner.x
    runner_y = runner.y

    # Get neighbors we can get to without being blocked by walls
    walls_around = get_walls(maze, runner_x, runner_y)
    reachable_neighbors = []
    # Add north cell if reachable
    if not walls_around[0]:
        reachable_neighbors.append("N")
    # Add east cell if reachable
    if not walls_around[1]:
        reachable_neighbors.append("E")
    # Add south cell if reachable
    if not walls_around[2]:
        reachable_neighbors.append("S")
    # Add west cell if reachable
    if not walls_around[3]:
        reachable_neighbors.append("W")

    # Map directions to find coordinates for flood fill values
    directions_offsets = {
        "N": (runner_x, runner_y + 1),
        "E": (runner_x + 1, runner_y),
        "S": (runner_x, runner_y - 1),
        "W": (runner_x - 1, runner_y),
    }

    # Find values for each reachable neighbor cell
    neighbor_values = {}
    for neighbor in reachable_neighbors:
        neighbor_coordinates = directions_offsets[neighbor]
        neighbor_x = neighbor_coordinates[0]
        neighbor_y = neighbor_coordinates[1]
        if 0 <= neighbor_x < maze.width and 0 <= neighbor_y < maze.height:
            neighbor_value = values[neighbor_y][neighbor_x]
            neighbor_values[neighbor] = neighbor_value

    # Find best direction with lowest flood fill value
    best_direction = None
    lowest_value = float("inf")
    for key, value in neighbor_values.items():
        if value < lowest_value:
            lowest_value = value
            best_direction = key

    current_orientation = runner.orientation
    # In only reachable wall outside maze bounds no best direction so keep default
    if best_direction is None:
        best_direction = current_orientation

    # Look at orientations as a clock and find out how many clockwise steps need from one direction to another
    orientations = ["N", "E", "S", "W"]
    target_orientation = best_direction
    current_orientation_index = orientations.index(current_orientation)
    target_orientation_index = orientations.index(target_orientation)

    # Move runner in best direction
    steps = (
        target_orientation_index - current_orientation_index
    ) % 4  # mod 4 for wraparound like a real clock
    if steps == 1:
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        actions = "RF"
    elif steps == 2:
        runner = turn(runner, "Right")
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        actions = "B"
    # 3 clockwise steps same as 1 anticlockwise step
    elif steps == 3:
        runner = turn(runner, "Left")
        runner = go_straight(runner, maze)
        actions = "LF"
    # Otherwise runner didn't have to move to just go forward
    else:
        runner = go_straight(runner, maze)
        actions = "F"

    runner_and_actions = (runner, actions, values)
    return runner_and_actions


def explore(
    runner: Runner,
    maze: Maze,
    goal: Optional[Tuple[int, int]] = None,
    scribe: bool = True,
) -> List[Tuple[int, int, str]]:

    # If no target make it top right corner
    if goal is None:
        goal = (maze.width - 1, maze.height - 1)

    values = compute_flood_fill(maze, goal)

    # For part 6 if we scribe journey open file where we will write it
    scribe_file = None
    writer = None
    if scribe:
        scribe_file = open("exploration.csv", "w", newline="")
        writer = csv.writer(scribe_file)
        writer.writerow(["Step", "x-coordinate", "y-coordinate", "Actions"])

    runner_x = runner.x
    runner_y = runner.y

    step = 1
    movements = []
    visited_states = set()

    while (runner.x, runner.y) != goal:
        runner, actions, values = move(runner, maze, values)

        # state = (runner.x, runner.y, runner.orientation)

        # if state in visited_states:
        #     # Endless loop, no wall around for left hug algorithm
        #     break

        # visited_states.add(state)

        current_coordinates_actions = (runner_x, runner_y, actions)
        movements.append(current_coordinates_actions)

        # In part 6 write to scribe file
        if scribe:
            writer.writerow([step, runner_x, runner_y, actions])

        step += 1

        # Update runner coordinates
        runner_x = runner.x
        runner_y = runner.y

    if scribe:
        scribe_file.close()

    return movements
