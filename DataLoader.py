"""Class for data import from file"""

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
        """Load data from file to class attributes using updated parser"""
        with open(self._file_path, "r") as f:
            lines = f.read().splitlines()
            if not lines:
                raise ValueError("File is empty or unreadable.")

        m, n = map(int, lines[0].split())
        self._n = m +1
        self._m = n +1

        costs = []
        idx = 1
        while len(costs) < n:
            costs.extend(map(int, lines[idx].split()))
            idx += 1
        self._costs = costs

        element_covers = [[] for _ in range(self._n)]
        current_element = 1
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
            #element_covers.append([x for x in entries])  # 1-based
            element_covers[current_element].extend(entries)
            current_element += 1
            idx += 1
        self._element_covers = element_covers

        subset_covers = [set() for _ in range(n)]
        for elem_index, subsets in enumerate(element_covers):
            for subset in subsets:
                subset_covers[subset - 1].add(elem_index + 1)  # switch back to 1-based

        self._subset_covers = [sorted(list(s)) for s in subset_covers]


    def get_n(self) -> int:
        """Get number of elements that need to be covered

        Returns:
            int: Number of elements that need to be covered
        """
        return self._n

    def get_m(self) -> int:
        """Get number of subsets

        Returns:
            int: Number of subsets in instance
        """
        return self._m
    
    def get_element_covers(self) -> list[list[int]]:
        """Return list of subsets covering each element

        Returns:
            List[List[int]]: List of subsets covering each element
        """
        return self._element_covers

    def get_subset_covers(self) -> list[list[int]]:
        """Return list of elements covered by each subset

        Returns:
            List[List[int]]: List of elements covered by each subset
        """

        return self._subset_covers
    
    def get_costs(self) -> list[int]:
        """Return cost of each subset

        Returns:
            List[int]: List of costs per subset
        """
        return self._costs


if __name__ == "__main__":
    print("Testing DataLoader...")
    dl = DataLoader("scp_toy.txt")
    dl.fetch_data()
    for i in range(dl.get_n()):
        print(f"Element {i} is covered by subsets: {dl.get_element_covers()[i]}")
    a = 1 + None