import functools
from itertools import pairwise, product

from tqdm import tqdm

KEYPAD_NUMERICAL = {
    "7": (0, 0), "8": (0, 1), "9": (0, 2),
    "4": (1, 0), "5": (1, 1), "6": (1, 2),
    "1": (2, 0), "2": (2, 1), "3": (2, 2),
                 "0": (3, 1), "A": (3, 2),
}

KEYPAD_DIRECTIONAL = {
                 "^": (0, 1), "A": (0, 2),
    "<": (1, 0), "v": (1, 1), ">": (1, 2),
}

COORDS_NUMERICAL = set(KEYPAD_NUMERICAL.values())
COORDS_DIRECTIONAL = set(KEYPAD_DIRECTIONAL.values())

# Load the codes from the input file
codes: list[str]
with open("input_21.txt", "r") as f:
    codes = [
        code
        for line in f.readlines()
        if (code := line.strip())
    ]


def coords_to_directional_instructions(
        from_coords: tuple[int, int],
        to_coords: tuple[int, int],
        options: set[tuple[int, int]]
) -> set[str]:
    if from_coords not in options:
        return set()

    dy, dx = to_coords[0] - from_coords[0], to_coords[1] - from_coords[1]
    if dy == 0 and dx == 0:
        return {"A"}

    res: set[str] = set()
    if dx > 0:
        res = res.union([
            ">" + instr for instr in coords_to_directional_instructions(
                (from_coords[0], from_coords[1] + 1),
                to_coords,
                options,
            )
        ])
    if dx < 0:
        res = res.union([
            "<" + instr for instr in coords_to_directional_instructions(
                (from_coords[0], from_coords[1] - 1),
                to_coords,
                options,
            )
        ])
    if dy > 0:
        res = res.union([
            "v" + instr for instr in coords_to_directional_instructions(
                (from_coords[0] + 1, from_coords[1]),
                to_coords,
                options,
            )
        ])
    if dy < 0:
        res = res.union([
            "^" + instr for instr in coords_to_directional_instructions(
                (from_coords[0] - 1, from_coords[1]),
                to_coords,
                options,
            )
        ])

    return res


def numerical_to_directional(came_from: str, target: str) -> set[str]:
    from_coords = KEYPAD_NUMERICAL[came_from]
    to_coords = KEYPAD_NUMERICAL[target]
    return coords_to_directional_instructions(from_coords, to_coords, COORDS_NUMERICAL)


@functools.cache
def directional_to_directional(came_from: str, target: str) -> set[str]:
    from_coords = KEYPAD_DIRECTIONAL[came_from]
    to_coords = KEYPAD_DIRECTIONAL[target]
    return coords_to_directional_instructions(from_coords, to_coords, COORDS_DIRECTIONAL)


LAYERS = [
    # Part A
    numerical_to_directional,
    *[directional_to_directional] * 2,
    # Part B
    *[directional_to_directional] * 23,
]

def find_instructions(code: str, *, layer: int) -> set[str]:
    options = find_instructions(code, layer=layer-1) if layer > 0 else {code}
    res = set()
    for option in options:
        paths = [""]
        for prev, to in pairwise("A" + option):
            paths = [
                "".join(combination)
                for combination in product(paths, LAYERS[layer](prev, to))
            ]

        res = res.union(paths)
        shortest = min(map(len, res))
        res = set(list(filter(lambda p: len(p) == shortest, res))[:2])

    return res


total = 0
for code in codes:
    options = find_instructions(code, layer=2)
    option = next(iter(options))
    complexity = len(option) * int(code[:-1])
    total += complexity

print("Part A:", total)


# ##
# # Part 2
# ##
total = 0
for code in tqdm(codes):
    options = find_instructions(code, layer=25)
    option = next(iter(options))
    complexity = len(option) * int(code[:-1])
    total += complexity

print("Part B:", total)
