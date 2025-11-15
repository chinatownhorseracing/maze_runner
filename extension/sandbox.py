width = 9
height = 5

values = []
# For each row
for i in range(height):
    row = []
    # For each element in row
    for j in range(width):
        row.append(None)
    values.append(row)

for row in values:
    print(row)
