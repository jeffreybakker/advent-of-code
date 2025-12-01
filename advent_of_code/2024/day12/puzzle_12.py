from itertools import count
from typing import Annotated

from tqdm import tqdm

type Coords = tuple[int, int]
type Farm = tuple[
    Annotated[set[Coords], "tiles"],
    Annotated[list[Coords], "perimeter"]
]

grid: dict[Coords, str] = {}
grid_width: int = 0
grid_height: int = 0
with open("input_12.txt") as f:
    for y, line in enumerate(f.readlines()):
        line = line.strip()
        if not line:
            continue

        grid_height = y + 1
        for x, c in enumerate(line):
            grid_width = x + 1
            grid[(y, x)] = c

# All directions in which we can search/walk
DIRECTIONS = {(0, 1), (0, -1), (1, 0), (-1, 0)}


def search(start: Coords) -> Farm:
    tiles: set[Coords] = {start}
    perimeter: list[Coords] = []

    start_tile = grid[start]
    queue: set[Coords] = {start}
    while len(queue) > 0:
        item = queue.pop()

        # Verify that it is of the same type we are searching for
        if grid.get(item, None) != start_tile:
            continue

        # Search the neighbouring directions
        y, x = item
        for yy, xx in DIRECTIONS:
            neighbour = (y + yy, x + xx)

            # Skip if it is already visited
            if neighbour in tiles or neighbour in queue:
                continue

            # If it is a different character, then it must be perimeter
            if grid.get(neighbour, None) != start_tile:
                perimeter.append(neighbour)
                continue

            tiles.add(neighbour)
            queue.add(neighbour)

    return tiles, perimeter


# Search all farms
farms: list[Farm] = []
visited: set[Coords] = set()
for y, x in tqdm([(y, x) for y in range(grid_height) for x in range(grid_width)]):
    # Skip visited tiles
    if (y, x) in visited:
        continue

    farm = search((y, x))
    farms.append(farm)

    # Mark all tiles of this farm as visited
    visited = visited.union(farm[0])

# Count the total fences required for part A
total = 0
for tiles, perimeter in farms:
    total += len(tiles) * len(perimeter)

print("Part A:", total)


# ##
# # Part 2
# ##
total = 0
for tiles, perimeter in tqdm(farms):
    sides = 0

    # Sort the perimeter tiles so we only have to search down and to the right
    perimeter = sorted(perimeter)
    perimeter_sides = {
        (y, x): {
            (yy, xx) for yy, xx in DIRECTIONS
            if (y + yy, x + xx) in tiles
        }
        for y, x in perimeter
    }
    while len(perimeter) > 0:
        sides += 1

        # Take the next perimeter item to check
        y, x = coords = perimeter.pop(0)

        # Take a direction to check
        dy, dx = direction = perimeter_sides[coords].pop()
        if direction[0] != 0:
            # top/bottom side, move horizontally
            search_direction = ((y, x + i) for i in count(start=1))
        else:
            # left/right side, move vertically
            search_direction = ((y + i, x) for i in count(start=1))

        # Walk along this direction
        for yy, xx in search_direction:
            # Test if we are still on the perimeter
            if (yy, xx) not in perimeter:
                break

            # Check if there is still a tile in the chosen direction
            expected_tile_coords = (yy + dy, xx + dx)
            if expected_tile_coords not in tiles:
                break

            # Remove this tile from
            perimeter.remove((yy, xx))
            perimeter_sides[(yy, xx)].remove((dy, dx))

    total += len(tiles) * sides

print("Part B:", total)
