from copy import copy

dense: list[int]
with open("input_9.txt", "r") as f:
    dense = [int(char) for char in f.read().strip()]

sparse: list[int | None] = []
empty_blocks: list[tuple[int, int]] = []  # Needed for part B
last_id = -1
for i, count in enumerate(dense):
    # Full blocks for even i
    if i % 2 == 0:
        last_id += 1
        sparse += [last_id] * count
    # Empty blocks for every uneven i
    else:
        empty_blocks.append((len(sparse), count))
        sparse += [None] * count

defragmented: list[int | None] = copy(sparse)
i, j = 0, len(defragmented) - 1
while i < j:
    # Increment i until we find an empty spot in memory
    if defragmented[i] is not None:
        i += 1
        continue

    # Decrement j until we find a non-empty spot in memory
    if defragmented[j] is None:
        j -= 1
        continue

    # If we have a valid combination of i and j, then swap their contents
    defragmented[i], defragmented[j] = defragmented[j], defragmented[i]

checksum = 0
for i, block_id in enumerate(defragmented):
    if block_id is None:
        break
    checksum += i * block_id

print("Part A:", checksum)


# ##
# # Part 2
# ##
# Create another copy of the sparse memory for working
defragmented: list[int | None] = copy(sparse)
moved_files: set[int] = set()
i = len(defragmented) - 1
while i > 0:
    # Skip empty blocks
    if defragmented[i] is None or defragmented[i] in moved_files:
        i -= 1
        continue

    # Count how long the block is
    j = i - 1
    while j >= 0 and defragmented[j] == defragmented[i]:
        j -= 1

    length = i - j

    # Try to find a block of empty memory
    block_idx: int | None = None
    for block_idx, (block_start, block_length) in enumerate(empty_blocks):
        # Don't care about blocks
        if block_start >= i:
            break

        # Skip empty blocks that are too small
        if block_length < length or block_length <= 0:
            continue

        # Otherwise, we have found our block
        break

    # If we haven't found a block, then skip this file and continue
    if block_idx is None:
        i -= length
        continue

    # Modify the empty blocks list
    block_start, block_length = empty_blocks[block_idx]
    if block_length < length or block_start >= i:
        i -= length
        continue
    elif block_length == length:
        empty_blocks.pop(block_idx)
    else:
        empty_blocks[block_idx] = (block_start + length, block_length - length)

    moved_files.add(defragmented[i])

    # Move the file
    for j in range(length):
        defragmented[block_start + j], defragmented[i - j] = defragmented[i - j], defragmented[block_start + j]

    i -= length

checksum = 0
for i, block_id in enumerate(defragmented):
    if block_id is None:
        continue
    checksum += i * block_id

print("Part B:", checksum)
