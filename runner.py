# Import maze object and its function to help implement sense_walls for runner
from maze import Maze, get_walls, create_maze


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


def move(runner: Runner, maze: Maze) -> Tuple[Runner, str]:
    walls_around_runner = sense_walls(runner, maze)

    has_wall_left = walls_around_runner[0]
    has_wall_front = walls_around_runner[1]
    has_wall_right = walls_around_runner[2]

    # Prioritize going left, front, right, back in this order
    if not has_wall_left:
        runner = turn(runner, "Left")
        runner = go_straight(runner, maze)
        actions = "LF"
    elif not has_wall_front:
        runner = go_straight(runner, maze)
        actions = "F"
    elif not has_wall_right:
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        actions = "RF"

    # Walls front and both sides so dead end, return
    else:
        runner = turn(runner, "Right")
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        actions = "B"

    runner_and_actions = (runner, actions)
    return runner_and_actions


def explore(
    runner: Runner, maze: Maze, goal: Optional[Tuple[int, int]] = None
) -> List[Tuple[int, int, str]]:

    # If no target make it top right corner
    if goal is None:
        goal = (maze.width - 1, maze.height - 1)
    runner_x = runner.x
    runner_y = runner.y
    movements = []
    while (runner.x, runner.y) != goal:
        runner, actions = move(runner, maze)
        current_coordinates_actions = (runner_x, runner_y, actions)
        movements.append(current_coordinates_actions)
        runner_x = runner.x
        runner_y = runner.y
    return movements
