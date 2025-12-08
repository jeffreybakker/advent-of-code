from functools import cache

grid: list[str]
with open("input.txt", "r") as f:
    grid = [
        line
        for raw_line in f.readlines()
        if (line := raw_line.strip())
    ]

start_row = [idx for idx, row in enumerate(grid) if "S" in row][0]
start_col = grid[start_row].index("S")


##
# Part A
##
# Queue (and visited list) of (row, col)-tuples
queue: set[tuple[int, int]] = set()
visited: set[tuple[int, int]] = set()

# Add the start position to the queue
queue.add((start_row, start_col))

split_count = 0
while len(queue) > 0:
    y, x = queue.pop()

    # Skip if we've been here before
    if (y, x) in visited:
        continue

    # Skip item if it lies outside the grid...
    if y >= len(grid) or x < 0 or x >= len(grid[y]):
        continue

    tile = grid[y][x]
    visited.add((y, x))
    if tile == "^":
        split_count += 1
        queue.add((y, x-1))
        queue.add((y, x+1))
    else:
        queue.add((y+1, x))

print("Part A:", split_count)


##
# Part B
##
# Using @cache turns this into a dynamic programming solution (as it saves intermediate steps of the computation)
@cache
def detect_timelines(y: int, x: int) -> int:
    # Return 1 timeline if we've exited the grid
    if y >= len(grid) or x < 0 or x >= len(grid[y]):
        return 1

    tile = grid[y][x]
    if tile == "^":
        return detect_timelines(y, x-1) + detect_timelines(y, x+1)
    else:
        return detect_timelines(y+1, x)


print("Part B:", detect_timelines(start_row, start_col))
