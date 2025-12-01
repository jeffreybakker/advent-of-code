from enum import Enum
from itertools import count

import numpy as np
from tqdm import tqdm


class Tile(int, Enum):
    EMPTY = 0
    WALL = 1
    BOX = 2

    # For part 2
    BOX_LEFT = 3
    BOX_RIGHT = 4


RAW_DIRECTIONS: dict[str, tuple[int, int]] = {
    "<": (0, -1),  # Move left
    ">": (0, 1),  # Move right
    "^": (-1, 0),  # Move up
    "v": (1, 0),  # Move down
}

# Read the input
grid_raw: list[list[Tile]] = []
moves: list[tuple[int, int]] = []
start_position: tuple = (-1, -1)  # [y, x]
with open("input_15.txt") as f:
    lines = iter(line.strip() for line in f.readlines())

    # First load the grid
    for y, line in enumerate(lines):
        # Empty line means we move on to the robot's moves
        if not line:
            break

        row: list[Tile] = []
        grid_raw.append(row)
        for x, char in enumerate(line):
            if char == "#":
                row.append(Tile.WALL)
            elif char == "O":
                row.append(Tile.BOX)
            elif char == "@":
                start_position = (y, x)
                row.append(Tile.EMPTY)
            else:
                row.append(Tile.EMPTY)

    for line in lines:
        if not line:
            continue

        moves.extend([RAW_DIRECTIONS[c] for c in line])

# Cleanup variables we won't be using anymore
del line, lines, f, row, char, y, x

# Let the robot do its thing
grid = np.array(grid_raw, dtype=np.int_)
position = np.array(start_position, dtype=np.int_)
for move in tqdm(map(lambda x: np.array(x, dtype=np.int_), moves)):
    next_position = position + move

    # Do different things depending on what we encounter
    tile = grid[tuple(next_position)]
    if tile == Tile.WALL:
        # We cannot move through walls, so skip
        continue
    elif tile == Tile.BOX:
        # Try to move the box to the first empty tile
        moved_box = False
        for i in count(start=1):
            other_position = next_position + i * move
            other_tile = grid[tuple(other_position)]
            if other_tile == Tile.WALL:
                break
            elif other_tile != Tile.EMPTY:
                continue

            # Swap contents
            grid[tuple(next_position)], grid[tuple(other_position)] = other_tile, tile
            moved_box = True
            break

        # Skip updating position if we couldn't move the box
        if not moved_box:
            continue

    # Update position and continue
    position = next_position

print("Puzzle A:", np.argwhere(grid == Tile.BOX).dot([100, 1]).sum())

# ##
# # Part 2
# ##
# First construct the wide grid
grid_wide = np.zeros((grid.shape[0], grid.shape[1] * 2), dtype=np.int_)
for y, row in enumerate(grid_raw):
    for x, tile in enumerate(row):
        if tile != Tile.BOX:
            grid_wide[y, x * 2:x * 2 + 2] = tile
        else:
            grid_wide[y, x * 2] = Tile.BOX_LEFT
            grid_wide[y, x * 2 + 1] = Tile.BOX_RIGHT

del y, x, row, tile


def find_connected_boxes_x(start: np.ndarray, direction: np.ndarray) -> set[tuple[int, int]]:
    boxes: set[tuple[int, int]] = set()
    for i in count(start=0):
        pos = start + direction * i
        tile = grid_wide[tuple(pos)]
        if tile == Tile.WALL:
            return boxes
        elif tile == Tile.EMPTY:
            return boxes

        boxes.add(tuple(pos))


def find_connected_boxes_y(start: np.ndarray, direction: np.ndarray) -> set[tuple[int, int]]:
    tile = grid_wide[tuple(start)]
    if tile == Tile.EMPTY or tile == Tile.WALL:
        return set()

    # Find both halves of the box
    box = [start]
    if tile == Tile.BOX_LEFT:
        box.append(start + np.array([0, 1]))
    else:
        box.append(start + np.array([0, -1]))

    res = set(map(tuple, box))
    for box_pos in box:
        res = res.union(find_connected_boxes_y(box_pos + direction, direction))

    return res


position = np.array(start_position, dtype=np.int_) * np.array([1, 2])
for move in tqdm(map(lambda x: np.array(x, dtype=np.int_), moves)):
    next_position = position + move

    # Do different things depending on what we encounter
    tile = grid_wide[tuple(next_position)]
    if tile == Tile.WALL:
        # We cannot move through walls, so skip
        continue
    elif tile == Tile.BOX_LEFT or tile == Tile.BOX_RIGHT:
        # Find all boxes influenced by this move
        boxes_coords = np.array(
            list(find_connected_boxes_x(next_position, move))
            if move[0] == 0 else
            list(find_connected_boxes_y(next_position, move)),
            dtype=np.int_
        )

        # Retrieve the boxes from the grid and empty their positions
        boxes = grid_wide[boxes_coords[:, 0], boxes_coords[:, 1]]
        grid_wide[boxes_coords[:, 0], boxes_coords[:, 1]] = Tile.EMPTY

        # Test if the boxes can be placed at their new positions
        boxes_coords_new = boxes_coords + move
        if np.any(grid_wide[boxes_coords_new[:, 0], boxes_coords_new[:, 1]] != Tile.EMPTY):
            # Not possible, so place the boxes back and skip
            grid_wide[boxes_coords[:, 0], boxes_coords[:, 1]] = boxes
            continue
        else:
            # Otherwise move the boxes to their new locations
            grid_wide[boxes_coords_new[:, 0], boxes_coords_new[:, 1]] = boxes

    # Update position and continue
    position = next_position

print("Puzzle B:", np.argwhere(grid_wide == Tile.BOX_LEFT).dot([100, 1]).sum())
