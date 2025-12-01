import functools
from typing import Callable, Generator, Iterable

inputs: list[int]
with open("input_11.txt", "r") as f:
    inputs = list(map(int, f.read().strip().split(" ")))


def flat_map(fn: Callable[[int], list[int]], items: Iterable[int]) -> Generator[int, None, None]:
    return (res for item in items for res in fn(item))


def apply_rules(x: int) -> list[int]:
    if x == 0:
        return [1]

    str_x = str(x)
    if len(str_x) % 2 == 0:
        middle = len(str_x) // 2
        return [int(str_x[:middle]), int(str_x[middle:])]

    return [x * 2024]


res = inputs
for i in range(25):
    res = flat_map(apply_rules, res)

print("Part A:", len(list(res)))


# ##
# # Part 2
# ##
@functools.cache
def apply(x: int, n: int) -> int:
    if n == 0:
        return 1

    return sum(apply(y, n-1) for y in apply_rules(x))


res = sum(apply(x, 75) for x in inputs)
print("Part B:", res)
