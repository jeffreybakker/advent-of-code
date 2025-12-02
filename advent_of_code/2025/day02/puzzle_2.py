import re
from typing import Iterator

from tqdm import tqdm

ranges: list[tuple[int, int]]
with open("input_a.txt", "r") as f:
    items = (
        f.read()
        .replace("\n", "")
        .replace("\r", "")
        .replace("\t", "")
        .replace(" ", "")
        .split(",")
    )

    # noinspection PyTypeChecker
    ranges = [
        tuple(map(int, item.split("-")))
        for item in items
    ]

    del items


def find_invalid_ids(pattern: str) -> Iterator[int]:
    compiled_pattern = re.compile(pattern)
    for (start, end) in tqdm(ranges):
        for nr in range(start, end + 1):
            if compiled_pattern.fullmatch(str(nr)) is not None:
                yield nr


print("Part A:", sum(find_invalid_ids(r"([0-9]+)\1")))
print("Part B:", sum(find_invalid_ids(r"([0-9]+)\1+")))
