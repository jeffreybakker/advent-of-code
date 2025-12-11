from functools import cache

graph: dict[str, set[str]]
with open('input.txt', 'r') as f:
    graph = {
        items[0].strip(":"): set(items[1:])
        for raw_line in f.readlines()
        if (line := raw_line.strip()) and (items := line.split(" "))
    }


START = "svr"


##
# Part A
##
@cache
def find_paths(current: str) -> int:
    if current == "out":
        return 1

    return sum(find_paths(child) for child in graph[current])

print("Part A:", find_paths(START))


##
# Part B
##
@cache
def find_valid_paths(current: str, visited_fft: bool = False, visited_dac: bool = False) -> int:
    if current == "out":
        return 1 if visited_fft and visited_dac else 0

    return sum(
        find_valid_paths(child, visited_fft or current == "fft", visited_dac or current == "dac")
        for child in graph[current]
    )


print("Part B:", find_valid_paths(START))
