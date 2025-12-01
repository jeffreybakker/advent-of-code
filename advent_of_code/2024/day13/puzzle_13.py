from typing import Annotated

import numpy as np
from tqdm import tqdm

type Coords = tuple[Annotated[int, "X"], Annotated[int, "Y"]]
type Challenge = tuple[
    Annotated[Coords, "A"],
    Annotated[Coords, "B"],
    Annotated[Coords, "Q"],
]

challenges: list[Challenge] = []
with open("input_13.txt", "r") as f:
    lines = iter(line.strip() for line in f.readlines())
    while True:
        try:
            line = next(lines)
        except StopIteration:
            break

        if not line:
            continue
        elif not line.startswith("Button A:"):
            raise ValueError("Unexpected line: " + line)

        a: Coords = tuple(map(int, line.removeprefix("Button A: X+").split(", Y+")))
        b: Coords = tuple(map(int, next(lines).removeprefix("Button B: X+").split(", Y+")))
        q: Coords = tuple(map(int, next(lines).removeprefix("Prize: X=").split(", Y=")))

        challenges.append((a, b, q))

del f, lines, line, a, b, q

total_costs = 0
for (ax, ay), (bx, by), (qx, qy) in tqdm(challenges):
    # Check all possible counts of A presses (where the remaining sum can be solved by B)
    a_options = np.arange(min(101, qx // ax + 1), dtype=np.int64)
    a_options = a_options[(qx - a_options * ax) % bx == 0]
    a_options = a_options[(qy - a_options * ay) % by == 0]

    # How many times B would have to be pressed
    b_options = (qx - a_options * ax) // bx

    # Ensure the sum matches target location Y (`by` has not been tested yet)
    valid_options = (
        (ax * a_options + bx * b_options == qx)
        & (ay * a_options + by * b_options == qy)
    )
    a_options, b_options = a_options[valid_options], b_options[valid_options]

    # Remove options with more than 100 presses per button
    valid_options = (a_options <= 100) & (b_options <= 100)
    a_options, b_options = a_options[valid_options], b_options[valid_options]

    # Count the cost of this prize
    costs = a_options * 3 + b_options
    total_costs += costs.min() if costs.shape[0] > 0 else 0

print("Part A:", total_costs)


# ##
# # Part 2
# ##
total_costs = 0
for (ax, ay), (bx, by), (qx, qy) in tqdm(challenges):
    step_sizes = np.array([[ax, bx], [ay, by]], dtype=np.int64)
    target = np.array([qx, qy], dtype=np.int64) + 10000000000000

    # Solve for x: step_sizes * x = target
    solution = np.linalg.solve(step_sizes, target)

    # Drop all non-integer solutions (with threshold for floating point errors)
    if np.any(np.abs(solution - np.round(solution)) > 1e-3):
        continue

    a, b = tuple(map(int, np.round(solution)))
    total_costs += a * 3 + b

print("Part B:", total_costs)
