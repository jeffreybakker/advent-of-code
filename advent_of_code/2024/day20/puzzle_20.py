from collections import defaultdict
from enum import Enum
from itertools import count

from tqdm import tqdm


class Tile(int, Enum):
    EMPTY = 0
    WALL = 1


grid: list[list[Tile]] = []
start: tuple[int, int] = (-1, -1)
finish: tuple[int, int] = (-1, -1)
with open("input_20.txt", "r") as f:
    for y, line in enumerate(f.readlines()):
        line = line.strip()
        if not line:
            continue

        row: list[Tile] = []
        grid.append(row)
        for x, char in enumerate(line):
            if char == "#":
                row.append(Tile.WALL)
            elif char == ".":
                row.append(Tile.EMPTY)
            elif char == "S":
                start = (y, x)
                row.append(Tile.EMPTY)
            elif char == "E":
                finish = (y, x)
                row.append(Tile.EMPTY)

del f, x, y, line, row

DIRECTIONS = {(-1, 0), (1, 0), (0, -1), (0, 1)}

# [coords; dist from start]; the track
track: dict[tuple[int, int], int] = {}
track[start] = 0
y, x = start
for i in count(start=1):
    if finish in track:
        break

    for dy, dx in DIRECTIONS:
        pos = y + dy, x + dx
        if pos in track:
            continue

        tile = grid[pos[0]][pos[1]]
        if tile != Tile.EMPTY:
            continue

        track[pos] = i
        y, x = pos
        break


def find_cheats(max_length: int = 2) -> dict[tuple[int, int], dict[tuple[int, int], int]]:
    cheats = defaultdict(lambda: defaultdict(int))
    for begin, begin_idx in tqdm(track.items()):
        begin_cheats = cheats[begin]
        for end, end_idx in track.items():
            if begin == end:
                continue

            if end in begin_cheats:
                continue

            dist = abs(begin[0] - end[0]) + abs(begin[1] - end[1])
            if dist > max_length:
                continue

            profit = end_idx - begin_idx - dist
            if profit > 0:
                begin_cheats[end] = profit

    return cheats


def count_cheats(cheats: dict[tuple[int, int], dict[tuple[int, int], int]], min_profit: int = 100) -> int:
    cheat_len: dict[int, int] = defaultdict(int)
    for begin, begin_cheats in cheats.items():
        for end, profit in begin_cheats.items():
            cheat_len[profit] += 1

    return sum(n for length, n in cheat_len.items() if length >= min_profit)

print("Part A:", count_cheats(find_cheats()))
print("Part B:", count_cheats(find_cheats(max_length=20)))
