"""Class for data import from file"""

import os


class DataLoader:
    file_path = ""
    n: int
    m: int
    covers: list[list[int]]
    costs: list[int]
    reverse_covers: list[list[int]]

    def __init__(self, file_path: str) -> None:
        """Initialize with path to instance file

        Args:
            file_path (str): Path to instance file
        """
        base_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(base_dir, "instances", file_path)

    def fetch_data(self) -> None:
        """Load data from file to class attributes using updated parser"""
        with open(self.file_path, "r") as f:
            lines = f.read().splitlines()
            if not lines:
                raise ValueError("File is empty or unreadable.")

        m, n = map(int, lines[0].split())
        self.n = m
        self.m = n

        costs = []
        idx = 1
        while len(costs) < n:
            costs.extend(map(int, lines[idx].split()))
            idx += 1
        self.costs = costs

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
            element_covers.append([x - 1 for x in entries])  # zero-based
            idx += 1

        covers = [set() for _ in range(n)]
        for elem_index, col_list in enumerate(element_covers):
            for col in col_list:
                covers[col].add(elem_index + 1)  # switch back to 1-based

        self.covers = [sorted(list(s)) for s in covers]

    def get_n(self) -> int:
        """Get number of elements that need to be covered

        Returns:
            int: Number of elements that need to be covered
        """
        return self.n

    def get_m(self) -> int:
        """Get number of subsets

        Returns:
            int: Number of subsets in instance
        """
        return self.m

    def get_covers(self) -> list[list[int]]:
        """Return list of elements covered by each subset

        Returns:
            List[List[int]]: List of elements covered by each subset
        """

        return self.covers

    def get_costs(self) -> list[int]:
        """Return cost of each subset

        Returns:
            List[int]: List of costs per subset
        """
        return self.costs

    def get_reverse_covers(self) -> list[list[int]]:
        # Implement
        return self.reverse_covers


if __name__ == "__main__":
    print("Testing DataLoader...")
    dl = DataLoader("scp41.txt")
    dl.fetch_data()
    print(dl.get_covers()[0])
