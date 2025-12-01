import itertools
from collections import defaultdict
from typing import Mapping

import numpy as np
from tqdm import tqdm

grid_raw: list[str] = []
with open("input_8.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        grid_raw.append(line)


def make_grid(raw: list[str]) -> np.ndarray[tuple[int, int], np.dtype[int]]:
    grid = np.zeros((len(raw), len(raw[0])), dtype=int)

    for i, row in enumerate(raw):
        for j, char in enumerate(row):
            if char in {".", "#"}:
                continue
            grid[i, j] = ord(char)

    return grid


grid = make_grid(grid_raw)

all_antennas = np.argwhere(grid > 0)
antennas: Mapping[str, list[np.ndarray]] = defaultdict(list)
for antenna in all_antennas:
    char = chr(grid[tuple(antenna)])
    antennas[char].append(antenna)


def is_in_grid(point: np.ndarray) -> bool:
    return not np.any((point < 0) | (point >= np.array(grid.shape)))


antinodes: set[tuple[int, int]] = set()
for char, antenna_coords in tqdm(antennas.items()):
    for a, b in itertools.permutations(antenna_coords, 2):
        delta = a - b
        coord = a + delta
        if not is_in_grid(coord):
            continue

        antinodes.add(tuple(coord))

print("Part A:", len(antinodes))

antinodes: set[tuple[int, int]] = set()
for char, antenna_coords in tqdm(antennas.items()):
    for a, b in itertools.combinations(antenna_coords, 2):
        delta = a - b

        # Multiply normalized delta by any number k
        k = np.arange(max(*grid.shape) * 2 + 1, dtype=np.int_) - max(*grid.shape)
        k = np.repeat(k.reshape((k.shape[0], 1)), 2, axis=1)
        coords = a + k * np.repeat(delta.reshape((1, 2)), k.shape[0], axis=0)

        # Add valid coordinates to the list of antinodes
        valid_coords = np.apply_along_axis(is_in_grid, 1, coords)
        for i in np.argwhere(valid_coords)[:, 0]:
            antinodes.add(tuple(coords[i]))

print("Part B:", len(antinodes))

print()
print()
for y in range(grid.shape[0]):
    for x in range(grid.shape[1]):
        cell = grid[y, x]
        if cell > 0:
            print(chr(cell), end="")
        elif (x, y) in antinodes:
            print("#", end="")
        else:
            print(".", end="")
    print()
