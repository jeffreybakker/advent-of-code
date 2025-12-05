import numpy as np

grid_raw: list[list[bool]] = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        row = [char == "@" for char in line]
        grid_raw.append(row)

del row, line
grid = np.array(grid_raw, dtype=np.int_)
width, height = grid.shape


##
# Part A
##
def is_accessible(x: int, y: int) -> bool:
    # Check if given coordinates lie within the grid
    if x < 0 or x >= width or y < 0 or y >= height:
        # If not, return false
        return False

    tile: int = grid[x][y]
    if not tile:
        # Return false if it is not a roll
        return False

    # Determine the window to look at
    x_min = max(x - 1, 0)
    x_max = min(x + 2, width)

    y_min = max(y - 1, 0)
    y_max = min(y + 2, height)

    area = grid[x_min:x_max, y_min:y_max]

    # Return true if there are fewer than 4 rolls in the area (+1 for the currently selected tile)
    return np.sum(area) < 4 + 1


accessible = sum(is_accessible(x, y) for x in range(width) for y in range(height))
print("Part A:", accessible)


##
# Part B
##
# We're going to create a queue of paper rolls to remove, and whenever a roll is removed, all newly
# accessible neighbours will be added to the queue. Continue this process until the queue is empty...

# Start with a queue of all accessible items
queue: set[tuple[int, int]] = set((x, y) for x in range(width) for y in range(height) if is_accessible(x, y))

removed = 0
while len(queue) > 0:
    x, y = queue.pop()

    # Remove the paper roll from the grid
    grid[x, y] = 0
    removed += 1

    for dx in [-1, 0, 1]:
        for dy in [-1, 0, 1]:
            xx, yy = x + dx, y + dy

            # If the neighbour is accessible, add it to the queue (queue/set is unique so no need to check
            # if it is already in there)
            if is_accessible(xx, yy):
                queue.add((xx, yy))

print("Part B:", removed)
