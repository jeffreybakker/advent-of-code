from collections import defaultdict
from copy import copy
from typing import Generator, Mapping

import numpy as np

grid_raw: list[list[int]] = []
with open("input_10.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        grid_raw.append([int(x) for x in line])

grid: np.ndarray[tuple[int, int], np.dtype[np.int_]] = np.array(grid_raw)
_neighbour_directions: list[tuple[int, int]] = [
    (1, 0),
    (-1, 0),
    (0, 1),
    (0, -1),
]


def neighbours(coords: tuple[int, int]) -> Generator[tuple[int, int], None, None]:
    y, x = coords
    for yy, xx in _neighbour_directions:
        item = y + yy, x + xx

        # Check whether coords lie within grid
        if np.any((np.array(item) < 0) | (np.array(item) >= np.array(grid.shape))):
            continue

        yield item


starting_points: set[tuple[int, int]] = set(map(lambda x: tuple(map(int, x)), np.argwhere(grid == 0)))
queue = copy(starting_points)
visited: Mapping[tuple[int, int], set[tuple[int, int]]] = defaultdict(set)
while len(queue) > 0:
    coords = queue.pop()
    height = grid[coords]

    for neighbour_coords in neighbours(coords):
        neighbour_height = grid[neighbour_coords]

        # Skip any neighbours that aren't exactly 1 level higher
        if neighbour_height - height != 1:
            continue

        # Register this element as successor of the current item
        visited[coords].add(neighbour_coords)

        # Only en-queue this neighbour if it hasn't been visited yet (or isn't queued already)
        if neighbour_coords in visited or neighbour_coords in queue:
            continue

        queue.add(neighbour_coords)


def reachable_tops(coords: tuple[int, int]) -> set[tuple[int, int]]:
    if grid[coords] == 9:
        return {coords}

    res = set()
    for neighbour in visited[coords]:
        res = res.union(reachable_tops(neighbour))

    return res


print("Part A:", sum(map(lambda x: len(reachable_tops(x)), starting_points)))


# ##
# # Part 2
# ##
def total_trails(coords: tuple[int, int]) -> int:
    if grid[coords] == 9:
        return 1

    return sum(map(total_trails, visited[coords]))


print("Part B:", sum(map(total_trails, starting_points)))
