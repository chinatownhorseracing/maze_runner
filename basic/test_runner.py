import pytest
from runner import (
    create_runner,
    Runner,
    get_x,
    get_y,
    get_orientation,
    turn,
    forward,
    sense_walls,
    go_straight,
    move,
    explore,
)
from maze import create_maze, add_horizontal_wall, add_vertical_wall


def test_create_runner():

    # Test runner with default values
    runner = create_runner()
    assert isinstance(runner, Runner)
    assert runner.x == 0
    assert runner.y == 0
    assert runner.orientation == "N"

    # Test runner with non-default values
    runner = create_runner(1, 2, "E")
    assert isinstance(runner, Runner)
    assert runner.x == 1
    assert runner.y == 2
    assert runner.orientation == "E"


# Default x should be 0
def test_get_x():
    runner = create_runner()
    assert get_x(runner) == 0


# Default y should be 0
def test_get_y():
    runner = create_runner()
    assert get_y(runner) == 0


# Default orientation should be N
def test_get_orientation():
    runner = create_runner()
    assert get_orientation(runner) == "N"


def test_turn() -> None:
    # Test standard case
    runner = create_runner("N")
    runner = turn(runner, "Right")
    assert get_orientation(runner) == "E"

    # Test wraparound from start to end of directions list
    runner = create_runner("N")
    runner = turn(runner, "Left")
    assert get_orientation(runner) == "W"

    # Test wraparound from end to start of directions list
    runner = create_runner(0, 0, "W")
    runner = turn(runner, "Right")
    assert get_orientation(runner) == "N"


def test_forward() -> None:

    # Test upward movement
    runner = create_runner(0, 0, "N")
    runner = forward(runner)
    assert get_x(runner) == 0
    assert get_y(runner) == 1

    # Test downward movement
    runner = create_runner(0, 1, "S")
    runner = forward(runner)
    assert get_x(runner) == 0
    assert get_y(runner) == 0

    # Test left movement
    runner = create_runner(1, 0, "W")
    runner = forward(runner)
    assert get_x(runner) == 0
    assert get_y(runner) == 0

    # Test right movement
    runner = create_runner(0, 0, "E")
    runner = forward(runner)
    assert get_x(runner) == 1
    assert get_y(runner) == 0


def test_sense_walls():

    # Use figure maze for tests
    maze = create_maze(11, 5)

    # Test if runner sees random inexistent wall in middle
    runner = create_runner(5, 2, "E")
    assert sense_walls(runner, maze) == (False, False, False)

    # Test if runner sees wall to his left
    runner = create_runner(5, 4, "E")
    assert sense_walls(runner, maze) == (True, False, False)

    # Test if runner sees wall in his front
    runner = create_runner(4, 0, "S")
    assert sense_walls(runner, maze) == (False, True, False)

    # Test if runner sees wall to his right
    runner = create_runner(10, 3, "N")
    assert sense_walls(runner, maze) == (False, False, True)

    # Test if runner sees more than 1 wall
    runner = create_runner(0, 4, "W")
    assert sense_walls(runner, maze) == (False, True, True)


def test_go_straight():

    # Use figure maze
    maze = create_maze(11, 5)

    # Test if runner goes straight horizontally if no wall in front
    runner = create_runner(5, 2, "E")
    runner = go_straight(runner, maze)
    assert get_x(runner) == 6
    assert get_y(runner) == 2

    # Test if runner goes straight vertically if no wall in front
    runner = create_runner(5, 2, "N")
    runner = go_straight(runner, maze)
    assert get_x(runner) == 5
    assert get_y(runner) == 3

    # Test if runner goes straight horizontally if vertical wall in front
    runner = create_runner(5, 2, "E")
    maze = add_vertical_wall(maze, 2, 6)
    # Error raised, no move
    with pytest.raises(ValueError):
        go_straight(runner, maze)
    assert get_x(runner) == 5
    assert get_y(runner) == 2

    # Test if runner goes straight vertically if horizontal wall in front
    runner = create_runner(5, 2, "S")
    maze = add_horizontal_wall(maze, 5, 2)
    # Error raised, no move
    with pytest.raises(ValueError):
        go_straight(runner, maze)
    assert get_x(runner) == 5
    assert get_y(runner) == 2


def test_move():

    # Use figure maze
    maze = create_maze(11, 5)

    # Test if runner moves left if no wall left
    runner = create_runner(5, 2, "N")
    walls_around_runner = sense_walls(runner, maze)
    wall_left_before_moving = walls_around_runner[0]
    runner, actions = move(runner, maze)
    # If before moving no left wall check left turn+forward
    if not wall_left_before_moving:
        assert get_x(runner) == 4
        assert get_y(runner) == 2
        assert get_orientation(runner) == "W"
        assert actions == "LF"

    # Test runner moves forward if wall to the left, no wall front
    runner = create_runner(5, 2, "N")
    maze = add_vertical_wall(maze, 2, 5)
    walls_around_runner = sense_walls(runner, maze)
    wall_left_before_moving = walls_around_runner[0]

    runner, actions = move(runner, maze)

    if wall_left_before_moving:
        assert get_x(runner) == 5
        assert get_y(runner) == 3
        assert get_orientation(runner) == "N"
        assert actions == "F"

    # Test if runner moves right if wall left, wall front, no wall right
    runner = create_runner(5, 2, "N")
    maze = add_vertical_wall(maze, 2, 5)
    maze = add_horizontal_wall(maze, 5, 3)
    walls_around_runner = sense_walls(runner, maze)
    wall_left_before_moving = walls_around_runner[0]
    wall_front_before_moving = walls_around_runner[1]
    wall_right_before_moving = walls_around_runner[2]

    runner, actions = move(runner, maze)
    # Should do right turn + forward
    if (
        wall_left_before_moving
        and wall_front_before_moving
        and not wall_right_before_moving
    ):
        assert get_x(runner) == 6
        assert get_y(runner) == 2
        assert get_orientation(runner) == "E"
        assert actions == "RF"

    # Test if runner turns around, moves 1 step back right if wall left, wall front, wall right
    maze = create_maze(11, 5)
    runner = create_runner(5, 2, "N")
    maze = add_vertical_wall(maze, 2, 5)
    maze = add_horizontal_wall(maze, 5, 3)
    maze = add_vertical_wall(maze, 2, 6)
    walls_around_runner = sense_walls(runner, maze)
    wall_left_before_moving = walls_around_runner[0]
    wall_front_before_moving = walls_around_runner[1]
    wall_right_before_moving = walls_around_runner[2]

    runner, actions = move(runner, maze)
    # Should do right turn + forward
    if (
        wall_left_before_moving
        and wall_front_before_moving
        and wall_right_before_moving
    ):
        assert get_x(runner) == 5
        assert get_y(runner) == 1
        assert get_orientation(runner) == "S"
        assert actions == "B"


def test_explore():
    # Test longest left hug algorithm if runner starts with relative left wall
    maze = create_maze(11, 5)
    runner = create_runner(10, 3, "S")
    runner_positions_actions = explore(runner, maze)
    assert runner_positions_actions == [
        (10, 3, "F"),
        (10, 2, "F"),
        (10, 1, "F"),
        (10, 0, "RF"),
        (9, 0, "F"),
        (8, 0, "F"),
        (7, 0, "F"),
        (6, 0, "F"),
        (5, 0, "F"),
        (4, 0, "F"),
        (3, 0, "F"),
        (2, 0, "F"),
        (1, 0, "F"),
        (0, 0, "RF"),
        (0, 1, "F"),
        (0, 2, "F"),
        (0, 3, "F"),
        (0, 4, "RF"),
        (1, 4, "F"),
        (2, 4, "F"),
        (3, 4, "F"),
        (4, 4, "F"),
        (5, 4, "F"),
        (6, 4, "F"),
        (7, 4, "F"),
        (8, 4, "F"),
        (9, 4, "F"),
    ]

    # Test if left hug works if goal not in default position
    maze = create_maze(11, 5)
    runner = create_runner()
    runner_positions_actions = explore(runner, maze, (10, 3))
    assert runner_positions_actions == [
        (0, 0, "F"),
        (0, 1, "F"),
        (0, 2, "F"),
        (0, 3, "F"),
        (0, 4, "RF"),
        (1, 4, "F"),
        (2, 4, "F"),
        (3, 4, "F"),
        (4, 4, "F"),
        (5, 4, "F"),
        (6, 4, "F"),
        (7, 4, "F"),
        (8, 4, "F"),
        (9, 4, "F"),
        (10, 4, "RF"),
    ]
