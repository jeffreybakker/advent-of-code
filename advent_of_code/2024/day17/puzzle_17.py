from enum import Enum
from itertools import count

import numpy as np
from tqdm import trange

registers_init: list[int] = []
program: list[int] = []
with open("input_17.txt", "r") as f:
    lines = iter(line.strip() for line in f.readlines())

    # First read the initial register values
    for line in lines:
        if not line:
            break

        value = int(line.split(": ")[1])
        registers_init.append(value)

    # Read the program
    for line in lines:
        if not line:
            break

        program = list(map(int, line.removeprefix("Program: ").split(",")))

del f, lines, line, value


class OpCode(int, Enum):
    ADV = 0
    BXL = 1
    BST = 2
    JNZ = 3
    BXC = 4
    OUT = 5
    BDV = 6
    CDV = 7


def execute_program(registers: list[int]) -> list[int]:
    registers = list(registers)
    output: list[int] = []
    program_counter = 0
    for _ in count():
        if program_counter >= len(program):
            break

        op = OpCode(program[program_counter])
        arg = program[program_counter+1]

        # Parse the operation's argument
        arg_literal = arg
        arg_combo: int = arg
        if arg_combo == 7:
            arg_combo = None
        elif arg_combo > 3:
            arg_combo = registers[arg_combo-4]

        # Increase the program counter (so it may be overridden by the jump)
        program_counter += 2

        if op == OpCode.ADV:
            registers[0] = int(registers[0] / (2**arg_combo))
        elif op == OpCode.BXL:
            registers[1] = registers[1] ^ arg_literal
        elif op == OpCode.BST:
            registers[1] = arg_combo % 8
        elif op == OpCode.JNZ:
            if registers[0] != 0:
                program_counter = arg_literal
        elif op == OpCode.BXC:
            registers[1] = registers[1] ^ registers[2]
        elif op == OpCode.OUT:
            output.append(arg_combo % 8)
        elif op == OpCode.BDV:
            registers[1] = int(registers[0] / (2**arg_combo))
        elif op == OpCode.CDV:
            registers[2] = int(registers[0] / (2**arg_combo))
        else:
            raise ValueError(f"Unknown opcode {op}")

    return output


print("Part A:", ",".join(map(str, execute_program(registers_init))))


# ##
# # Part 2
# ##
# No inspiration for a general solution yet, but will try to solve the input
# So first, we explore a pattern in values of A that yield correct outputs
# for i in trange(1000000):
#     out = execute_program([i, 0, 0])
#     if np.array_equal(out, program[-len(out):]):
#         print(i, out)

# EXAMPLE: There is a pattern in here, about *8 every step (every acceptable
# value is a range of 8 possible values, starting at n)
# 0     0
# 3     24        +24
# 5     224       +200        * 8.333
# 5     1832      +1608       * 8.04
# 6     14680     +12848      * 7.9900
# 1     117440    +102760     * 7.9981

# Which is correct, B and C are dependent on A, and A is divided by 8 every time
# a, b, c = 25358015, 0, 0
# while a > 0:
#     b = a % 8
#     b = b ^ 1
#     c = int(a / (2 ** b))
#     a = int(a / (2 ** 3))
#     b = b ^ c
#     b = b ^ 6
#     print(b % 8)

queue = list(range(8))
while len(queue) > 0:
    i = queue.pop(0)
    out = execute_program([i, 0, 0])
    match = np.array_equal(out, program[-len(out):])
    if match and len(out) == len(program):
        found = True
        print(i, out)
        print("Part B:", i)
        break
    elif match:
        print(i, out)
        options = [i * 8 + j for j in range(8)]
        queue.extend(options)
