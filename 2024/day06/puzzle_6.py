from enum import Enum
from functools import lru_cache
from itertools import count
from multiprocessing import get_context
from time import sleep
from typing import Optional

import numpy as np


class LoopException(BaseException):
    pass


class Tile(int, Enum):
    EMPTY = 0
    OBSTACLE = 1


class Direction(int, Enum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3


start_position: tuple[int, int] = (-1, -1)
start_direction: tuple[int, int] = (1, 0)
grid_raw: list[list[Tile]] = []
with open("input_6.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        line = line.strip()
        if not line:
            continue

        row: list[Tile] = []
        grid_raw.append(row)
        for x, tile in enumerate(line):
            if tile == ".":
                row.append(Tile.EMPTY)
            elif tile == "#":
                row.append(Tile.OBSTACLE)
            elif tile in {"^", "v", ">", "<"}:
                row.append(Tile.EMPTY)
                start_position = (y, x)
                if tile == "^":
                    start_direction = (-1, 0)
                elif tile == ">":
                    start_direction = (0, 1)
                elif tile == "v":
                    start_direction = (1, 0)
                elif tile == "<":
                    start_direction = (0, -1)
                else:
                    raise ValueError(f"Unknown direction: {tile}")
            else:
                raise ValueError(f"Unknown tile: {tile}")

del row, tile, x, y, line, f

directions = {
    Direction.NORTH: (-1, 0),
    Direction.EAST: (0, 1),
    Direction.SOUTH: (1, 0),
    Direction.WEST: (0, -1),
}


@lru_cache
def lookup_direction(direction: tuple[int, int]) -> Direction:
    for dir, delta in directions.items():
        if direction == delta:
            return dir

    raise ValueError(f"Direction not found: {direction}")


def rotate_right(direction: np.ndarray) -> np.ndarray:
    return np.array([direction[1], -direction[0]])


def walk(
        grid: np.ndarray,
        position: np.ndarray,
        direction: np.ndarray,
        visited: Optional[np.ndarray] = None,
) -> np.ndarray:
    if visited is None:
        visited = np.zeros((*grid.shape, 4), dtype=np.int32)

    direction_idx = lookup_direction(tuple(direction))
    visited[(*position, direction_idx)] = np.max(visited) + 1
    for step in count(start=np.max(visited) + 1):
        # Determine the next position
        next_position = position + direction

        # Stop if the next position would lie outside of the board
        if np.any(next_position < np.zeros_like(position)) or np.any(next_position >= np.array(grid.shape)):
            break

        # Test what the tile at the next position would be
        next_tile = grid[tuple(next_position)]

        # Rotate 90 degrees right if we encounter an obstacle
        if next_tile == Tile.OBSTACLE:
            direction = rotate_right(direction)
            visited[(*position, lookup_direction(tuple(direction)))] = step
            continue

        # Test if we have visited the next tile already
        direction_idx = lookup_direction(tuple(direction))
        if visited[(*next_position, direction_idx)] > 0:
            raise LoopException()

        # Finally, update the position, leave a visited marker, and continue
        position = next_position
        visited[(*position, direction_idx)] = step

    return visited


grid = np.array(grid_raw)
visited = walk(
    grid=grid,
    position=np.array(start_position),
    direction=np.array(start_direction),
)
print("Tiles visited:", np.sum(visited.sum(axis=-1) > 0))


# ##
# # Part 2
# ##
def check_option(option) -> tuple[int, int] | None:
    y, x, direction_idx = option
    position = np.array([y, x])
    direction = np.array(directions[direction_idx])
    step = visited[y, x, direction_idx]

    next_position = position + direction

    # We cannot place an obstacle at the original start position
    if np.array_equal(next_position, np.array(start_position)):
        return None

    # Check if next position would be out-of-bounds
    if np.any(next_position < np.zeros_like(position)) or np.any(next_position >= np.array(grid.shape)):
        return None

    # Skip if there is already an obstacle there
    next_tile = grid[tuple(next_position)]
    if next_tile == Tile.OBSTACLE:
        return None

    # We cannot place an obstacle if we had to visit it earlier in our walk
    visited_in_steps = visited[tuple(next_position)]
    if np.any((visited_in_steps > 0) & (visited_in_steps < step)):
        return None

    # Then try what happens when we place an obstacle there
    option = np.array(grid_raw)
    option[tuple(next_position)] = Tile.OBSTACLE

    visited_seed = np.copy(visited)
    visited_seed[visited >= step] = 0
    try:
        walk(grid=option, position=position, direction=direction, visited=visited_seed)
        return None
    except LoopException:
        return tuple(next_position)


sleep(0.1)

with get_context("fork").Pool() as pool:
    options = set(pool.map(check_option, np.argwhere(visited > 0)))

options.remove(None)
print(len(options))
