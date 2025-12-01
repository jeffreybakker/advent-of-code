from itertools import count
from pathlib import Path

import numpy as np
from matplotlib import pyplot as plt, animation
import seaborn as sns
from tqdm import tqdm

WIDTH = 101  # 11 (example), or 101 (puzzle input)
HEIGHT = 103  # 7 (example), or 103 (puzzle input)

robots: list[tuple[tuple[int, int], tuple[int, int]]] = []
with open("input_14.txt") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        p, v = line.split(" ")
        p = tuple(map(int, p.removeprefix("p=").split(",")))
        v = tuple(map(int, v.removeprefix("v=").split(",")))

        robots.append((p, v))

del f, line, p, v

positions = np.array([robot[0] for robot in robots], dtype=np.int64)
velocities = np.array([robot[1] for robot in robots], dtype=np.int64)

N_STEPS = 100

new_positions = (positions + N_STEPS * velocities) % np.array([WIDTH, HEIGHT])

quadrant_a = ((new_positions[:, 0] < WIDTH // 2) & (new_positions[:, 1] < HEIGHT // 2)).sum()
quadrant_b = ((new_positions[:, 0] < WIDTH // 2) & (new_positions[:, 1] > HEIGHT // 2)).sum()
quadrant_c = ((new_positions[:, 0] > WIDTH // 2) & (new_positions[:, 1] < HEIGHT // 2)).sum()
quadrant_d = ((new_positions[:, 0] > WIDTH // 2) & (new_positions[:, 1] > HEIGHT // 2)).sum()

print("Part A:", quadrant_a * quadrant_b * quadrant_c * quadrant_d)


# ##
# # Part 2
# ##
out_path = Path(__file__).parent / "part_b"
out_path.mkdir(parents=True, exist_ok=True)

for i in tqdm(count()):
    updated = (positions + i * velocities) % np.array([WIDTH, HEIGHT])

    fig, ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100))

    ax.scatter(
        x=updated[:, 0],
        y=updated[:, 1],
        s=1,
    )

    plt.savefig(str(out_path / f"{i}.jpg"), dpi=100)

    if i > 0 and np.array_equal(positions, updated):
        print(i)
        break


# fig, ax = plt.subplots(figsize=(WIDTH / 100, HEIGHT / 100))
#
# points = ax.scatter([], [], c="b", s=5)
# frame_nr = ax.text(0.05, 0.95, "0", transform=ax.transAxes)
# ax.set(xlim=(0, WIDTH), ylim=(0, HEIGHT))
#
#
# def update(frame):
#     data = (positions + frame * velocities) % np.array([WIDTH, HEIGHT])
#     points.set_offsets(data)
#     frame_nr.set_text(f"{frame}")
#
#     return points, frame_nr
#
#
# ani = animation.FuncAnimation(fig, update, frames=1000, interval=500)
# ani.save("puzzle_14.gif", writer="pillow")
