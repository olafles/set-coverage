import os
from collections import defaultdict
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import time

def load_scp(filename: str) -> tuple:
    """" Load set cover problem instance from file."""""
    filepath = os.path.join("instances", filename)
    with open(filepath, "r") as f:
        lines = f.readlines()

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

def greedy_set_cover_with_progress(costs: list, covers: list, m: int) -> tuple[list[int], list[int]]:
    """
    Algorytm zachłanny z zapisem liczby pokrytych elementów po każdej iteracji.
    """
    uncovered = set(range(m))
    selected = []
    coverage_progress = []

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

        selected.append(best + 1)
        uncovered -= covers[best]
        coverage_progress.append(m - len(uncovered))

    return selected, coverage_progress

def print_column_assignments(selected_columns: list, covers: list) -> None:
    """Prints the elements covered by selected columns."""
    for col in selected_columns:
        col_elements = covers[col - 1]
        print(f"Kolumna {col+1} pokrywa elementy: {sorted(col_elements)}")

def plot_column_cover_histogram(covers: list[set], selected_columns: list[int]) -> None:
    """
    Rysuje histogram liczby elementów pokrywanych przez każdą kolumnę,
    z zaznaczeniem kolumn wybranych przez algorytm greedy.
    """
    import matplotlib.pyplot as plt

    num_elements_per_col = [len(c) for c in covers]
    col_indices = list(range(1, len(covers) + 1))

    plt.figure(figsize=(15, 6))
    bars = plt.bar(col_indices, num_elements_per_col, color='lightgray', label='Pozostałe kolumny')

    # Zaznacz wybrane kolumny na czerwono
    for col in selected_columns:
        bars[col - 1].set_color('red')

    plt.xlabel("Kolumna (numer)")
    plt.ylabel("Liczba pokrywanych elementów")
    plt.title("Liczba elementów pokrywanych przez każdą kolumnę")
    plt.legend()
    plt.tight_layout()
    plt.show()

def greedy_set_cover_live(costs: list, covers: list, m: int) -> list[int]:
    """
    Algorytm zachłanny z dynamicznym wykresem postępu (na żywo).
    """
    uncovered = set(range(m))
    selected = []
    coverage_progress = []

    plt.ion()  # Tryb interaktywny
    fig, ax = plt.subplots(figsize=(10, 5))
    line, = ax.plot([], [], marker='o')
    ax.set_xlim(0, 20)  # początkowy zakres (można zmienić dynamicznie później)
    ax.set_ylim(0, m)
    ax.set_xlabel("Iteracja")
    ax.set_ylabel("Liczba pokrytych elementów")
    ax.set_title("Postęp pokrywania elementów przez greedy")
    ax.grid(True)

    iteration = 0

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

        selected.append(best + 1)
        uncovered -= covers[best]
        covered_count = m - len(uncovered)
        coverage_progress.append(covered_count)

        # Aktualizacja wykresu
        iteration += 1
        line.set_xdata(range(1, iteration + 1))
        line.set_ydata(coverage_progress)
        ax.set_xlim(0, max(10, iteration + 2))
        ax.set_ylim(0, m + 10)
        fig.canvas.draw()
        fig.canvas.flush_events()
        time.sleep(0.1)  # pauza, żeby zobaczyć efekt (można usunąć)

    plt.ioff()
    plt.show()

    return selected

m, n, costs, covers = load_scp('scp41.txt')

print(f"Liczba elementów do pokrycia: {m}")
print(f"Liczba kolumn (podzbiorów): {n}")
print(f"Koszt kolumny 420: {costs[420]}")

selected_columns = greedy_set_cover(costs, covers, m)
print(f"Wybrane kolumny: {selected_columns}")

print_column_assignments(selected_columns, covers)

column_to_elements = defaultdict(set)

for element_index, col_list in enumerate(covers):
    for col in col_list:
        column_to_elements[col].add(element_index + 1)

for col in sorted(column_to_elements.keys()):
    sorted_elements = sorted(column_to_elements[col])
    print(f"Element {col+1} jest pokrywany przez kolumny: {sorted_elements}")

def plot_coverage_progress(progress: list[int], m: int) -> None:
    """
    Rysuje wykres liczby pokrytych elementów po każdej iteracji greedy.
    """
    plt.figure(figsize=(10, 5))
    plt.plot(range(1, len(progress) + 1), progress, marker='o')
    plt.axhline(y=m, color='gray', linestyle='--', label='Pełne pokrycie')
    plt.xlabel("Iteracja")
    plt.ylabel("Liczba pokrytych elementów")
    plt.title("Postęp pokrywania elementów przez greedy")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

selected_columns = greedy_set_cover_live(costs, covers, m)