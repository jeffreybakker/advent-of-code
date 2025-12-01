# Extract the reports from the input file
import numpy as np
from tqdm import tqdm

reports: list[list[int]] = []
with open("input_2.txt", "r") as f:
    for line in f.readlines():
        line = line.strip()
        if not line:
            continue

        levels = map(int, line.split(" "))
        reports.append(list(levels))


def is_safe(report) -> bool:
    diff = np.diff(report, n=1)

    # A report is safe if adjacent levels differ at least one and at most three
    if np.any((np.abs(diff) < 1) | (np.abs(diff) > 3)):
        return False

    # A report is safe if all levels are increasing or decreasing
    increasing = np.all(diff > 0)
    decreasing = np.all(diff < 0)
    if not increasing and not decreasing:
        return False

    return True


# Count all safe reports
safe_reports = 0
for report in tqdm(reports):
    if not is_safe(report):
        continue

    # Add to the counter
    safe_reports += 1

print("Safe reports:", safe_reports)


# ##
# # Part 2
# ##
safe_reports_damped = 0
for report in tqdm(reports):
    # First test if the entire report is safe
    if is_safe(report):
        safe_reports_damped += 1
        continue

    # Otherwise test if it is safe by removing a single item
    for i in range(len(report)):
        if is_safe(report[:i] + report[i+1:]):
            safe_reports_damped += 1
            break

print("Safe reports (with dampener):", safe_reports_damped)
