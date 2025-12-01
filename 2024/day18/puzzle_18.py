from collections import defaultdict
from typing import Optional

import numpy as np

WIDTH = 71  # Example 7 or Input 71
HEIGHT = WIDTH
NEIGHBOUR_DIRS = {(0, 1), (0, -1), (1, 0), (-1, 0)}

corrupted_bytes: list[tuple[int, int]]
with open("input_18.txt", "r") as f:
    corrupted_bytes = [
        tuple(map(int, line.strip().split(",")))
        for line in f.readlines()
    ]


def a_star(start: tuple[int, int], target: tuple[int, int], n_corrupted_bytes: int) -> Optional[list[tuple[int, int]]]:
    came_from: dict[tuple[int, int], tuple[int, int]] = {}
    g_scores: dict[tuple[int, int], float] = defaultdict(lambda: float("inf"))
    f_scores: dict[tuple[int, int], float] = defaultdict(lambda: float("inf"))

    g_scores[start] = 0
    f_scores[start] = 0
    queue: set[tuple[int, int]] = {start}
    while len(queue) > 0:
        # Select the items from the queue with the lowest f-score
        sorted_queue = sorted(queue, key=lambda item: f_scores[item])
        y, x = current = sorted_queue[0]
        queue.remove(current)

        if current == target:
            break

        for dy, dx in NEIGHBOUR_DIRS:
            yy, xx = neighbour = y + dy, x + dx

            # Ensure coords are in grid
            if not (0 <= yy < HEIGHT and 0 <= xx < WIDTH):
                continue

            # Ensure tile is not corrupted
            if neighbour in corrupted_bytes[:n_corrupted_bytes]:
                continue

            neighbour_score = g_scores[current] + 1
            if neighbour_score < g_scores[neighbour]:
                came_from[neighbour] = current
                g_scores[neighbour] = neighbour_score
                f_scores[neighbour] = neighbour_score + abs(y - target[0]) + abs(x - target[1])
                if neighbour not in queue:
                    queue.add(neighbour)

    if target not in came_from:
        return None

    current = target
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.insert(0, current)

    return path


n_corrupted = 1024
print("Part A:", len(a_star((0, 0), (HEIGHT-1, WIDTH-1), n_corrupted)) - 1)


# ##
# # Part 2
# ##
previous = 0
path = a_star((0, 0), (HEIGHT-1, WIDTH-1), n_corrupted)
while path is not None:
    blocks_path = -1
    for i, coords in enumerate(corrupted_bytes[n_corrupted:], start=1):
        if coords not in path:
            continue

        blocks_path = n_corrupted + i
        break

    if blocks_path == -1:
        raise ValueError()

    n_corrupted = blocks_path
    path = a_star((0, 0), (HEIGHT-1, WIDTH-1), n_corrupted)

print("Part B:", ",".join(map(str, corrupted_bytes[n_corrupted-1])))
