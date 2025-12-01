import numpy as np
from tqdm import tqdm

equations: dict[int, np.ndarray] = {}
with open("input_7.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        solution, inputs = line.split(": ")
        equations[int(solution)] = np.array(list(map(int, inputs.split(" "))))


def can_solve(solution: int, numbers: np.ndarray[tuple[int], np.int_]) -> bool:
    if numbers.shape[0] == 1:
        return numbers[0] == solution
    elif solution < 0:
        return False

    # Grab the last element of the numbers
    init, last = numbers[:-1], numbers[-1]

    # *: test if solution is divisible by the last number, skip otherwise
    if solution % last == 0 and can_solve(solution // last, init):
        return True

    # +: otherwise, test addition
    return can_solve(solution - last, init)


total = 0
for solution, numbers in tqdm(equations.items()):
    if can_solve(solution, numbers):
        total += solution

print("Part A:", total)


# ##
# # Part 2
# ##
def can_solve2(solution: int, numbers: np.ndarray[tuple[int], np.int_]) -> bool:
    if numbers.shape[0] == 1:
        return numbers[0] == solution
    elif solution < 0:
        return False

    # Grab the last element of the numbers
    init, last = numbers[:-1], numbers[-1]

    # *: test if solution is divisible by the last number, skip otherwise
    if solution % last == 0 and can_solve2(solution // last, init):
        return True

    # +: otherwise, test addition operator
    if can_solve2(solution - last, init):
        return True

    # ||: finally, test combination operator
    n_digits = len(str(last))
    if solution % (10 ** n_digits) == last:
        return can_solve2(solution // (10 ** n_digits), init)


total = 0
rejected = []
for solution, numbers in tqdm(equations.items()):
    if can_solve2(solution, numbers):
        total += solution
    else:
        rejected.append((solution, numbers))

print("Part B:", total)
