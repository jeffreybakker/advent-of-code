import numpy as np
from tqdm import tqdm

# Extract the left and right lists from input
left, right = [], []
with open("input_1.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        a, b = line.split("   ")
        left.append(int(a))
        right.append(int(b))

# Convert to numpy arrays for easier computation
left = np.array(left)
right = np.array(right)

# Sort the two lists
left.sort()
right.sort()

print("Total difference:", np.sum(np.abs(left - right)))


# ##
# # Part 2
# ##
similarity = 0
for l in tqdm(left):
    similarity += l * (right == l).sum()

print("Similarity:", similarity)
