from pathlib import Path

path = Path(__file__).parent

instructions: list[int] = []
with open(str(path / "input_a.txt"), "r") as f:
    for line in f.readlines():
        line = line.strip().replace("L", "-").removeprefix("R")
        if not line:
            continue

        instructions.append(int(line))


def apply_instruction(position: int, instruction: int) -> tuple[int, int]:
    new_position = position + instruction
    through_zero = abs(new_position) // 100
    if new_position < 0 and position != 0 or new_position == 0:
        through_zero += 1

    return new_position % 100, through_zero


# Part A
starting_position = 50
current_position = starting_position
zeros = 0
for instruction in instructions:
    current_position, _ = apply_instruction(current_position, instruction)
    if current_position == 0:
        zeros += 1

print("Part A:", zeros)
# 1150


# Part B
def apply_iterative(position: int, instruction: int) -> tuple[int, int]:
    if instruction == 0:
        return position, 0

    direction = 1 if instruction > 0 else -1
    through_zero = 0
    while instruction != 0:
        position = (position + direction) % 100
        instruction -= direction

        if position == 0:
            through_zero += 1

    return position, through_zero


current_position = starting_position
zeros = 0
for instruction in instructions:
    if instruction == 0:
        continue

    current_position, passed_through_zero = apply_iterative(current_position, instruction)
    zeros += passed_through_zero

print("Part B:", zeros)
# 6835: too high
# 6265: too low
# 5420: too low
