import operator
from functools import reduce
from itertools import combinations, count

import numpy as np
from tqdm import tqdm, trange

type Coords = tuple[int, int, int]

boxes: list[Coords]
with open("input.txt", "r") as f:
    boxes = [
        tuple(map(int, line.split(",")))
        for raw_line in f.readlines()
        if (line := raw_line.strip())
    ]


##
# Part A
##
links: list[tuple[Coords, Coords, float]] = []
for i, a in tqdm(enumerate(boxes[:-1]), desc="Finding shortest links"):
    other_boxes = np.array(boxes[i+1:])
    difference = other_boxes - a
    distances = np.linalg.norm(difference, axis=1)
    shortest_indices = np.argsort(distances)
    for idx in shortest_indices:
        b = boxes[i + 1 + idx]
        dist = distances[idx]
        links.append((a, b, dist))

circuits: dict[Coords, set[Coords]] = {}
shortest_links = list(sorted(
    links,
    key=lambda x: x[2],
))


def _connect(a: Coords, b: Coords) -> set[Coords]:
    circuit_a = circuits.get(a, {a})
    circuit_b = circuits.get(b, {b})

    # Test if the junction boxes are in the same circuit
    if not circuit_a.difference(circuit_b):
        # If they are, then skip
        return circuit_a

    # Otherwise, merge the two and update the list of circuits
    circuit = circuit_a.union(circuit_b)
    for box in circuit:
        circuits[box] = circuit

    return circuit


for _ in trange(1000):
    a, b, _ = shortest_links.pop(0)
    _connect(a, b)

unique_circuits: set[tuple[Coords, ...]] = set(map(tuple, circuits.values()))
lengths = list(sorted(map(len, unique_circuits), reverse=True))
print("Part A:", reduce(operator.mul, lengths[:3]))


##
# Part B
##
for _ in tqdm(count()):
    a, b, _ = shortest_links.pop(0)
    circuit = _connect(a, b)
    if len(circuit) == len(boxes):
        break

ax, bx = a[0], b[0]
print("Part B:", ax * bx)
