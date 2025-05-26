"""This file contains class for data import from file (Singleton)"""

import os


class DataLoader:
    _file_path = ""
    _n: int
    _m: int
    _costs: list[int]
    _element_covers: list[list[int]]
    _subset_covers: list[list[int]]

    def __init__(self, file_path: str) -> None:
        """Initialize with path to instance file

        Args:
            file_path (str): Path to instance file
        """
        base_dir = os.path.dirname(__file__)
        self._file_path = os.path.join(base_dir, "instances", file_path)

    def fetch_data(self) -> None:
        """Load data from file to class attributes with zero-based indexing"""
        with open(self._file_path, "r") as f:
            lines = [line.strip() for line in f if line.strip()]
            if not lines:
                raise ValueError("File is empty or unreadable.")

        n_elements, n_subsets = map(int, lines[0].split())
        if n_elements <= 0 or n_subsets <= 0:
            raise ValueError(
                f"Invalid instance: n_elements={n_elements}, n_subsets={n_subsets}"
            )
        self._n = n_elements
        self._m = n_subsets

        costs: list[int] = []
        idx = 1
        while len(costs) < self._m and idx < len(lines):
            costs.extend(map(int, lines[idx].split()))
            idx += 1
        if len(costs) < self._m:
            raise ValueError(
                f"Not enough cost entries: expected {self._m}, got {len(costs)}"
            )
        self._costs = costs[: self._m]

        element_covers: list[list[int]] = []
        for _ in range(self._n):
            if idx >= len(lines):
                raise ValueError("Unexpected end of file when reading element covers.")
            parts = list(map(int, lines[idx].split()))
            idx += 1
            count = parts[0]
            entries = parts[1:]
            while len(entries) < count and idx < len(lines):
                entries.extend(map(int, lines[idx].split()))
                idx += 1
            if len(entries) < count:
                raise ValueError(
                    f"Not enough subset indices for element: expected {count}, got {len(entries)}"
                )
            element_covers.append([e - 1 for e in entries])

        self._element_covers = element_covers

        subset_covers: list[list[int]] = [[] for _ in range(self._m)]
        for elem_idx, subsets in enumerate(self._element_covers):
            for s in subsets:
                subset_covers[s].append(elem_idx)
        self._subset_covers = [sorted(lst) for lst in subset_covers]

    def get_n(self) -> int:
        """Get number of elements that need to be covered"""
        return self._n

    def get_m(self) -> int:
        """Get number of subsets"""
        return self._m

    def get_element_covers(self) -> list[list[int]]:
        """Return list of subsets covering each element"""
        return self._element_covers

    def get_subset_covers(self) -> list[list[int]]:
        """Return list of elements covered by each subset"""
        return self._subset_covers

    def get_costs(self) -> list[int]:
        """Return cost of each subset"""
        return self._costs

    def calculate_density(self) -> float:
        """Calculate the density of the instance"""
        subset_covers = self.get_subset_covers()
        total_elements_covered = sum(len(covers) for covers in subset_covers)
        density = (
            total_elements_covered / (self.get_m() * self.get_n()) * 100
            if self.get_m() > 0 and self.get_n() > 0
            else 0.0
        )
        return density


if __name__ == "__main__":
    # Testing
    dl = DataLoader("scp41.txt")
    dl.fetch_data()
    print(f"Loaded {dl.get_n()} elements and {dl.get_m()} subsets.")
    print(f"Costs: {dl.get_costs()}")
    print(f"Costs len: {len(dl.get_costs())}")
    print(f"Element covers sample: {dl.get_element_covers()}")
    print(f"Subset covers sample: {dl.get_subset_covers()}")
    print(f"Density: {dl.calculate_density():.2f}%")
