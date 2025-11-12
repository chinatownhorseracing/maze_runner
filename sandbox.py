positions = [
    (0, 0, "F"),
    (0, 2, "B"),
    (0, 3, "M"),
    (0, 5, "B"),
    (0, 9, "K"),
    (0, 3, "H"),
    (0, 4, "S"),
]
coordinates = [(x, y) for (x, y, actions) in positions]
already_seen_positions = []
already_seen_coordinates = []
length = len(positions)

for i in range(length):
    if coordinates[i] not in already_seen_coordinates:
        already_seen_coordinates.append(coordinates[i])
        already_seen_positions.append(positions[i])
    else:
        index_1st_repetition = already_seen_coordinates.index(coordinates[i])
        already_seen_coordinates[index_1st_repetition:] = []
        already_seen_coordinates.append(coordinates[i])
        already_seen_positions[index_1st_repetition:] = []
        already_seen_positions.append(positions[i])
print(already_seen_coordinates)
print(already_seen_positions)

# else:


#     else:
#         index = already_seen_positions.index(position)
#         print(index)
#         already_seen_positions[index:] = []
#         already_seen_positions.append(position)
# print(already_seen_positions)
