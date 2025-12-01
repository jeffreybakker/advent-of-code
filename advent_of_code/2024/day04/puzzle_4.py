import numpy as np
from tqdm import tqdm, trange

line_width: int = 0
text: str = ""

with open("input_4.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        line_width = len(line)
        text += line

directions: list[tuple[str, int]] = [
    ("N", -line_width),
    ("NE", -line_width + 1),
    ("E", 1),
    ("SE", line_width + 1),
    ("S", line_width),
    ("SW", line_width - 1),
    ("W", -1),
    ("NW", -line_width - 1),
]

target = "XMAS"
target_length = len(target)


def find_target(start_idx: int) -> int:
    start_x = start_idx % line_width

    res = 0
    for direction, delta in directions:
        # # Clipping on the x-axis
        if "W" in direction and start_x < target_length - 1:
            continue
        elif "E" in direction and start_x > line_width - target_length:
            continue

        elem = text[start_idx::delta][:target_length]
        if elem == target:
            res += 1

    return res


total = 0
for i in tqdm(range(len(text))):
    if text[i] != target[0]:
        continue
    total += find_target(i)

print("# of XMAS'es:", total)


# ##
# # Part 2
# ##
grid_raw: list[list[str]] = []
with open("input_4.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        grid_raw.append([line[i] for i in range(len(line))])

grid = np.array(grid_raw)
kernel = np.array(
    [
        ["M", None, "S"],
        [None, "A", None],
        ["M", None, "S"],
    ]
)
kernels = [np.rot90(kernel, k=i) for i in range(4)]


def test_kernels(area: np.ndarray) -> int:
    res = 0
    for kernel in kernels:
        match = True
        for i in range(kernel.shape[0]):
            for j in range(kernel.shape[1]):
                if kernel[i, j] is None:
                    continue

                if kernel[i, j] != area[i, j]:
                    match = False
                    break

            if not match:
                break

        if match:
            res += 1

    return res


total = 0
for y in trange(grid.shape[0] - 2):
    for x in range(grid.shape[1] - 2):
        total += test_kernels(grid[y:y+3, x:x+3])

print("# of X-MAS'es:", total)
