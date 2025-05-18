import os
from collections import defaultdict


def load_scp(path: str) -> tuple:
    """Load set cover problem instance from file."""
    with open(path, "r") as f:
        lines = f.read().splitlines()
        if not lines:
            raise ValueError("Plik jest pusty lub nie został poprawnie wczytany.")

    print(f"Załadowano {len(lines)} linii z pliku.")

    m, n = map(int, lines[0].split())

    costs = []
    idx = 1
    while len(costs) < n:
        costs.extend(map(int, lines[idx].split()))
        idx += 1

    element_covers = []
    while idx < len(lines):
        line = lines[idx].strip()
        if not line:
            idx += 1
            continue
        parts = list(map(int, line.split()))
        count = parts[0]
        entries = parts[1:]
        while len(entries) < count:
            idx += 1
            entries += list(map(int, lines[idx].split()))
        element_covers.append([x - 1 for x in entries])
        idx += 1

    covers = [set() for _ in range(n)]
    for elem_index, col_list in enumerate(element_covers):
        for col in col_list:
            covers[col].add(elem_index)

    return m, n, costs, covers
