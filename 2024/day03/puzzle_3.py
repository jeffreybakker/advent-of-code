import re

with open("input_3.txt", "r") as f:
    memory = f.read()

pattern = r"mul\([0-9]{1,3},[0-9]{1,3}\)"

result = 0
for x in re.finditer(pattern, memory):
    instruction = x.group().removeprefix("mul(").removesuffix(")")
    a, b = map(int, instruction.split(","))
    result += a * b

print("Output:", result)


# ##
# # Part 2
# ##
pattern = fr"({pattern})|(do\(\))|don\'t\(\)"
enabled = True
result = 0
for x in re.finditer(pattern, memory):
    match = x.group()

    if match.startswith("do("):
        enabled = True
    elif match.startswith("don't("):
        enabled = False
    elif match.startswith("mul("):
        # Skip if disabled
        if not enabled:
            continue

        instruction = x.group().removeprefix("mul(").removesuffix(")")
        a, b = map(int, instruction.split(","))
        result += a * b
    else:
        raise ValueError("Invalid instruction: " + match)

print("Output 2:", result)
