from collections import defaultdict

from tqdm import tqdm

connectivity: dict[str, set[str]] = defaultdict(set)
with open("input_23.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        a, b = line.split("-")
        connectivity[a].add(b)
        connectivity[b].add(a)

del f, line, a, b

groups3: set[tuple[str, str, str]] = set()
for node_a in tqdm(connectivity.keys()):
    if not node_a.startswith("t"):
        continue

    for node_b in connectivity[node_a]:
        intersection = connectivity[node_a].intersection(connectivity[node_b])
        for node_c in intersection:
            groups3.add(tuple(sorted({node_a, node_b, node_c})))

print("Part A:", len(groups3))


# ##
# # Part 2
# ##
groups: dict[str, list[set[str]]] = defaultdict(list)
for node, neighbours in tqdm(connectivity.items()):
    if node not in groups:
        groups[node].append({node})
        continue
