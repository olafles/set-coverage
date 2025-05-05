import os
from collections import defaultdict

def load_scp(path: str) -> tuple:
    """Load set cover problem instance from file."""
    with open(path, 'r') as f:
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

def greedy_set_cover(costs: list, covers: list, m: int) -> list:
    """Greedy algorithm for set cover problem."""
    uncovered = set(range(m))
    selected = []
    
    while uncovered:
        best = None
        best_efficiency = float('inf')

        for i, subset in enumerate(covers):
            newly_covered = uncovered.intersection(subset)
            if not newly_covered:
                continue
            efficiency = costs[i] / len(newly_covered)
            if efficiency < best_efficiency:
                best_efficiency = efficiency
                best = i
        
        if best is None:
            break

        selected.append(best+1)
        uncovered -= covers[best]

    return selected

def print_column_assignments(selected_columns: list, covers: list) -> None:
    """Prints the elements covered by selected columns."""
    for col in selected_columns:
        col_elements = covers[col - 1]
        print(f"Kolumna {col} pokrywa elementy: {sorted(col_elements)}")

m, n, costs, covers = load_scp('scp_toy.txt')

print(f"Liczba elementów do pokrycia: {m}")
print(f"Liczba kolumn (podzbiorów): {n}")
print(f"Koszt kolumny 0: {costs[0]}")

selected_columns = greedy_set_cover(costs, covers, m)

covered = set()
for col in selected_columns:
    covered |= covers[col-1]

missing = set(range(m)) - covered
if missing:
    print("Brakuje elementów:", missing)
else:
    print("Wszystkie elementy zostały pokryte.")
    print(f"Wybrane kolumny greedy: {selected_columns}")
    print_column_assignments(selected_columns, covers)

