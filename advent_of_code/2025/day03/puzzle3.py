import numpy as np

data_raw: list[list[str]] = []
with open("input.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        data_raw.append([char for char in line])

data = np.array(data_raw)

##
# Part A
##
jolts: list[int] = []
for line in data:
    highest_idx = np.argmax(line)
    if highest_idx >= len(line) - 1:
        second_highest_idx = np.argmax(line[:-1])
        jolts.append(int(line[second_highest_idx] + line[highest_idx]))
    else:
        second_highest_idx = np.argmax(line[highest_idx + 1:])
        jolts.append(int(line[highest_idx] + line[highest_idx + 1:][second_highest_idx]))

print("Part A:", sum(jolts))


##
# Part B
##
def solve(line: np.ndarray[tuple[int], np.dtype[np.str_]], n: int = 12) -> str:
    # Recursion: base case returns empty string
    if n <= 0:
        return ""

    # Select the highest one
    highest_idx = np.argmax(line)
    highest = str(line[highest_idx])

    if len(line) - highest_idx < n:
        # If there are <n remaining numbers after the highest one, continue the search on the left-side
        # of the line
        remaining = "".join(line[highest_idx + 1:])
        return solve(line[:highest_idx], n=n - (len(line) - highest_idx)) + highest + remaining
    else:
        # If there are >=n remaining numbers after the highest one, then continue the search on the
        # right-side of the line
        return str(line[highest_idx]) + solve(line[highest_idx+1:], n=n-1)

jolts = []
for line in data:
    jolts.append(solve(line, n=12))

print("Part B:", sum(map(int, jolts)))
