ranges: list[tuple[int, int]] = []
items: list[int] = []

with open("input.txt", "r") as f:
    lines = iter(f.readlines())
    for line in lines:
        line = line.strip()
        # Exit when we encounter an empty line (go to the next parsing step)
        if not line:
            break

        ranges.append(tuple(map(int, line.split("-"))))

    for line in lines:
        line = line.strip()
        if not line:
            continue

        items.append(int(line))


##
# Part A
##
def is_fresh(item: int) -> bool:
    for lo, hi in ranges:
        if lo <= item <= hi:
            return True

    return False


fresh_items = list(map(is_fresh, items))
print("Part A:", sum(fresh_items))


##
# Part B
##
# First, ensure the ranges are sorted
ranges_sorted = list(sorted(ranges))

total = 0
lo, hi = ranges_sorted.pop(0)
while True:
    try:
        # Take the next range (for comparison
        a, b = ranges_sorted.pop(0)
    except IndexError:
        # We've hit the end of the list, add the current range to the total
        total += hi - lo + 1
        break

    # If the two ranges overlap, then extend the current range
    if a <= hi + 1:
        hi = max(hi, b)
        continue

    # Otherwise, add the length of the current range to the total...
    total += hi - lo + 1

    # ... and adopt the new range
    lo, hi = a, b

print("Part B:", total)
