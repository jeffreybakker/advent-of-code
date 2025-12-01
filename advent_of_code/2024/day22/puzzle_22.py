from collections import defaultdict

from tqdm import tqdm

secrets: list[int]
with open("input_22.txt", "r") as f:
    secrets = [
        int(secret)
        for line in f.readlines()
        if (secret := line.strip())
    ]

# Create a binary mask from the prune-number (16777216 = 2^24)
BITMASK = 16777216 - 1


def apply(x: int) -> int:
    x = (x ^ (x << 6)) & BITMASK
    x = (x ^ (x >> 5)) & BITMASK
    x = (x ^ (x << 11)) & BITMASK
    return x


total = 0
for secret in tqdm(secrets):
    for _ in range(2000):
        secret = apply(secret)

    total += secret

print("Part A:", total)


# ##
# # Part 2
# ##
sequences: dict[tuple[int, int, int, int], int] = defaultdict(int)
for secret in tqdm(secrets):
    old_price = secret % 10

    found: set[tuple[int, int, int, int]] = set()
    sequence: tuple[int, int, int, int] = (0, 0, 0, 0)
    for i in range(2000):
        secret = apply(secret)

        price = secret % 10
        diff = price - old_price
        sequence = (*sequence[1:], diff)
        old_price = price

        # Starting at i=3, we can check sequences
        if i < 3:
            continue

        # We cannot use the same sequence twice
        if sequence in found:
            continue

        sequences[sequence] += price
        found.add(sequence)

print("Part B:", max(sequences.values()))
