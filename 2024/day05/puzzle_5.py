from collections import defaultdict
from typing import Mapping

from tqdm import tqdm

rules: Mapping[int, set[int]] = defaultdict(set)
updates: list[list[int]] = []
with open("input_5.txt", "r") as f:
    lines = iter(f.readlines())

    # First load all rules
    for line in lines:
        line = line.strip()
        # Empty line means we go on to the second part of the input
        if not line:
            break

        before, after = [int(x) for x in line.split("|")]
        rules[before].add(after)

    # Then load all updates
    for line in lines:
        line = line.strip()
        if not line:
            continue

        update = [int(x) for x in line.split(",")]
        updates.append(update)

total = 0
incorrect_updates: list[list[int]] = []
for update in tqdm(updates):
    correct = True
    for i, page_nr in enumerate(update):
        page_rules = rules[page_nr]
        previous = update[:i]
        if any(rule in previous for rule in page_rules):
            correct = False
            break

    if correct:
        total += update[len(update) // 2]
    else:
        incorrect_updates.append(update)

print("Part A:", total)


# ##
# # Part 2
# ##
def cmp(a: int, b: int) -> bool:
    return b in rules[a]


def merge_sort(items: list[int]) -> list[int]:
    # Base case
    if len(items) <= 1:
        return items

    # Split and recurse
    midpoint = len(items) // 2
    left, right = items[:midpoint], items[midpoint:]

    left = merge_sort(left)
    right = merge_sort(right)

    # Merge results
    res = []
    while len(left) > 0 and len(right) > 0:
        if cmp(left[0], right[0]):
            res.append(left.pop(0))
        else:
            res.append(right.pop(0))

    # Add the remaining items (one of the lists can still have items)
    res = res + left + right
    return res


total = 0
for update in tqdm(incorrect_updates):
    fixed = merge_sort(update)
    total += fixed[len(fixed) // 2]

print("Part B:", total)
