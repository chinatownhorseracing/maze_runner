from maze import Maze
from runner import explore, create_maze, create_runner


def shortest_path(
    maze: Maze,
    starting: Optional[Tuple[int, int]] = None,
    goal: Optional[Tuple[int, int]] = None,
) -> List[Tuple[int, int, str]]:
    if starting is None:
        starting = (0, 0)
    if goal is None:
        goal = (maze.width - 1, maze.height - 1)

    runner = create_runner()
    runner_positions_actions = explore(runner, maze)
    runner_positions_actions.insert(3, (0, 1, "F"))
    # print(runner_positions_actions)

    # Get all coordinates in path including duplicates
    runner_coordinates = [(x, y) for (x, y, actions) in runner_positions_actions]

    # Here will be stored positions+actions and coordinates already seen
    already_seen_positions_actions = []
    already_seen_coordinates = []

    length = len(runner_positions_actions)

    # For every position, action tuple in runner path
    for i in range(length):

        # If new coordinates add them to already seen list, also add the respective actions
        if runner_coordinates[i] not in already_seen_coordinates:
            already_seen_coordinates.append(runner_coordinates[i])
            already_seen_positions_actions.append(runner_positions_actions[i])
        else:
            # Used to delete everything from index of 1st repetition forward (the deadend path)
            index_1st_repetition = already_seen_coordinates.index(runner_coordinates[i])

            # Delete coordinates that led to dead end before returning to 2nd repetition of a coordinate
            # Also replace them with the new clean coordinates
            already_seen_coordinates[index_1st_repetition:] = []
            already_seen_coordinates.append(runner_coordinates[i])

            # Same as for coordinates but for the list containing both coordinates (positions) and actions
            already_seen_positions_actions[index_1st_repetition:] = []
            already_seen_positions_actions.append(runner_positions_actions[i])

    # The already_seen_positions_actions list was cleaned iteratively of dead ends now it's shortest path
    shortest_path = already_seen_positions_actions
    print(shortest_path)


maze = create_maze(11, 5)
best_path = shortest_path(maze)
print(best_path)


# maze = create_maze(11, 5)
# runner = create_runner()
# runner_positions_actions = explore(runner, maze)
# runner_positions_actions.insert(3, (0, 1, "F"))
# print(runner_positions_actions)

# # Get all coordinates in path including duplicates
# runner_coordinates = [(x, y) for (x, y, actions) in runner_positions_actions]

# # Here will be stored positions+actions and coordinates already seen
# already_seen_positions_actions = []
# already_seen_coordinates = []

# length = len(runner_positions_actions)

# # For every position, action in runner path
# for i in range(length):

#     # If new coordinates add them to already seen list, also add the respective actions
#     if runner_coordinates[i] not in already_seen_coordinates:
#         already_seen_coordinates.append(runner_coordinates[i])
#         already_seen_positions_actions.append(runner_positions_actions[i])
#     else:
#         # Used to delete everything from index of 1st repetition forward (the deadend path)
#         index_1st_repetition = already_seen_coordinates.index(runner_coordinates[i])

#         # Delete coordinates that led to dead end before returning to 2nd repetition of a coordinate
#         # Also replace them with the new clean coordinates
#         already_seen_coordinates[index_1st_repetition:] = []
#         already_seen_coordinates.append(runner_coordinates[i])

#         # Same as for coordinates but for the list containing both coordinates (positions) and actions
#         already_seen_positions_actions[index_1st_repetition:] = []
#         already_seen_positions_actions.append(runner_positions_actions[i])

# shortest_path = already_seen_positions_actions
# print(shortest_path)
