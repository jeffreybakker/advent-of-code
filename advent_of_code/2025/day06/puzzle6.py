import re
import operator
from functools import reduce
from typing import Callable

import numpy as np

instructions_raw: list[list[int]] = []
operations = list[str]
with open("input.txt", "r") as f:
    for line in f.readlines():
        line = re.sub(r"\s+", " ", line.strip())
        items = line.split(" ")

        if not items[0].isnumeric():
            operations = items
        else:
            instructions_raw.append(list(map(int, items)))

del line, items
instructions = np.array(instructions_raw)

ops: dict[str, Callable[[int, int], int]] = {
    "*": operator.mul,
    "+": operator.add,
}

##
# Part A
##
total = 0
for i in range(len(operations)):
    op = ops[operations[i]]
    result = reduce(op, instructions[:, i])
    total += result

print("Part A:", total)


##
# Part B
##
lines: list[str]
with open("input.txt", "r") as f:
    lines = [
        line
        for raw_line in f.readlines()
        if (line := raw_line.replace("\r", "").replace("\n", ""))
    ]

inst = lines[:-1]

total = 0

max_length = max(len(line) for line in lines)
index = 0
while index < max_length:
    op = ops[lines[-1][index]]
    items: list[int] = []
    while True:
        nr_str = "".join([line[index] for line in inst if index < len(line)]).strip()
        nr = int(nr_str) if nr_str else None
        index += 1
        if nr is not None:
            items.append(nr)
        else:
            break

    result = reduce(op, items)
    total += result

print("Part B:", total)
