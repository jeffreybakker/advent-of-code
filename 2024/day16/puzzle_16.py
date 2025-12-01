from collections import defaultdict
from enum import Enum


class Tile(int, Enum):
    EMPTY = 0
    WALL = 1
    TARGET = 2


class Direction(int, Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


DIRECTIONS: dict[Direction, tuple[int, int]] = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}

# Read the input
grid: list[list[Tile]] = []
start_position: tuple[int, int, Direction] = (-1, -1, Direction.EAST)  # [y, x, dir]
target_position: tuple[int, int] = (-1, -1)  # [y, x]
with open("input_16.txt") as f:
    for y, line in enumerate(f.readlines()):
        line = line.strip()
        if not line:
            continue

        row: list[Tile] = []
        grid.append(row)
        for x, char in enumerate(line):
            if char == "#":
                row.append(Tile.WALL)
            elif char == "E":
                target_position = (y, x)
                row.append(Tile.EMPTY)
            elif char == "S":
                start_position = (y, x, Direction.EAST)
                row.append(Tile.EMPTY)
            else:
                row.append(Tile.EMPTY)

del y, x, row, char, f, line


def neighbours(item: tuple[int, int, Direction]) -> list[tuple[int, int, Direction, int]]:
    res = []

    # Add forward move at cost 1
    dy, dx = DIRECTIONS[item[2]]
    res.append((item[0] + dy, item[1] + dx, item[2], 1))

    # Add rotation at cost 1000
    res.extend([
        (item[0], item[1], direction, 1000)
        for direction in DIRECTIONS.keys()
        if direction != item[2]
    ])

    return res


# Adjustment to A* nr.1: Keep track of multiple origins (as long as they share
# the same lowest score)
came_from: dict[tuple[int, int, Direction], set[tuple[int, int, Direction]]] = defaultdict(set)
g_scores: dict[tuple[int, int, Direction], float] = defaultdict(lambda: float("inf"))
f_scores: dict[tuple[int, int, Direction], float] = defaultdict(lambda: float("inf"))

g_scores[start_position] = 0
f_scores[start_position] = 0
queue: set[tuple[int, int, Direction]] = {start_position}
while len(queue) > 0:
    # Select the items from the queue with the lowest f-score
    sorted_queue = sorted(queue, key=lambda item: f_scores[item])
    lowest_score = f_scores[sorted_queue[0]]

    # Adjustment to A* nr.2: Process all items with the same lowest f-score at
    # the same time (before terminating). Works bc of Manhattan distance instead
    # of Euclidean distance
    items = [item for item in sorted_queue if f_scores[item] == lowest_score]
    for current in items:
        # Remove current item from the queue
        queue.remove(current)
        for y, x, direction, cost in neighbours(current):
            # Skip neighbour if it is a wall
            if grid[y][x] != Tile.EMPTY:
                continue

            neighbour = (y, x, direction)
            neighbour_score = g_scores[current] + cost
            if neighbour_score <= g_scores[neighbour]:
                # Either replace the origin when we found a new lowest way to
                # reach this neighbour
                if neighbour_score < g_scores[neighbour]:
                    came_from[neighbour] = {current}
                else:
                    # Or add a separate origin when they have the same score
                    came_from[neighbour].add(current)

                # Compute the new scores
                g_scores[neighbour] = neighbour_score
                # F-score with Manhattan distance metric
                f_scores[neighbour] = neighbour_score + abs(y - target_position[0]) + abs(x - target_position[1])

                if neighbour not in queue:
                    queue.add(neighbour)

    # Stop the exploration when we have reached the target node
    if any(item[:2] == target_position for item in items):
        break

target_node = [item for item in g_scores.keys() if item[:2] == target_position][0]
print("Part A:", g_scores[target_node])


# ##
# # Part 2
# ##
def find_paths(start: tuple[int, int, Direction]) -> set[tuple[int, int]]:
    res = {start[:2]}
    for item in came_from[start]:
        res = res.union(find_paths(item))

    return res


print("Part B:", len(find_paths(target_node)))
