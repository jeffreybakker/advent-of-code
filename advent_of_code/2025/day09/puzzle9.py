from concurrent.futures import ThreadPoolExecutor

import numpy as np
from tqdm import tqdm
import cv2 as cv

type Coords = tuple[int, int]

def parse_input() -> list[Coords]:
    red_tiles: list[Coords]
    with open("input.txt", "r") as f:
        return [
            tuple(map(int, line.split(",")))
            for raw_line in f.readlines()
            if (line := raw_line.strip())
        ]


##
# Part A
##
def find_areas(red_tiles: list[Coords]) -> list[tuple[Coords, Coords, int]]:
    tiles = np.array(red_tiles)
    combination_areas: list[tuple[Coords, Coords, int]] = []
    for i, a in tqdm(enumerate(red_tiles[:-1]), desc="Computing areas"):
        other_tiles = tiles[i + 1:]
        difference = np.abs(other_tiles - a) + 1
        areas = difference[:, 0] * difference[:, 1]
        for i, b in enumerate(other_tiles):
            combination_areas.append((a, tuple(map(int, b)), int(areas[i])))

    # Sort the areas by size (decreasing)
    combination_areas.sort(
        key=lambda x: x[2],
        reverse=True,
    )

    return combination_areas


##
# Part B
##
def initialize_grid(tiles: np.ndarray) -> np.ndarray:
    width, height = np.max(tiles[:, 0]) + 2, np.max(tiles[:, 1]) + 2
    grid = np.zeros((height, width), dtype=np.uint8)

    # Draw a polygon using OpenCV
    cv.fillPoly(grid, [tiles], color=(1,))

    # Convert to inverted boolean array (for performance reasons)
    return ~(grid.astype(np.bool_))


def _task_runner(grid: np.ndarray):
    global grid_inverted
    grid_inverted = grid


def _is_valid(task: tuple[Coords, Coords, int]) -> tuple[tuple[Coords, Coords, int], bool]:
    (ax, ay), (bx, by), area = task
    xmin, xmax = sorted((ax, bx))
    ymin, ymax = sorted((ay, by))
    rectangle = grid_inverted[ymin:ymax + 1, xmin:xmax + 1]

    return task, not np.any(rectangle)




if __name__ == "__main__":
    red_tiles = parse_input()
    combination_areas = find_areas(red_tiles)
    print("Part A:", combination_areas[0][-1])

    tiles = np.array(red_tiles)
    grid = initialize_grid(tiles)

    with ThreadPoolExecutor(max_workers=6, initializer=_task_runner, initargs=(grid,)) as executor:
    # with multiprocessing.get_context("spawn").Pool(processes=2, initializer=_task_runner, initargs=(grid,)) as executor:
        result = next(
            area
            for (a, b, area), is_all_tiled in tqdm(
                executor.map(_is_valid, combination_areas),
                total=len(combination_areas),
            )
            if is_all_tiled
        )

    print("Part B:", result)
