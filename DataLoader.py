"""Class for data import from file"""

import os


class DataLoader:
    file_path = ""
    n_rows: int
    rows = [int]
    n_columns: int
    columns = [[int]]
    costs = [int]

    def __init__(self, file_path: str) -> None:
        """Initialize with path to instance file

        Args:
            file_path (str): Path to instance file
        """
        base_dir = os.path.dirname(__file__)
        self.file_path = os.path.join(base_dir, "instances", file_path)

    def fetch_data(self) -> None:
        """Load data from file to class attributes"""
        with open(self.file_path, "r") as f:
            data = [int(x) for x in f.read().split()]

        it = iter(data)

        self.n_rows = next(it)
        self.n_columns = next(it)

        self.costs = [next(it) for _ in range(self.n_columns)]

        row_to_cols = []
        for _ in range(self.n_rows):
            k = next(it)
            cols = [next(it) for _ in range(k)]
            row_to_cols.append(cols)

        col_to_rows = [[] for _ in range(self.n_columns)]
        for row_idx, cols in enumerate(row_to_cols, start=1):
            for col in cols:
                col_to_rows[col - 1].append(row_idx)

        self.rows = list(range(1, self.n_rows + 1))
        self.columns = col_to_rows


if __name__ == "__main__":
    print("siema")
    dl = DataLoader("scp41.txt")
    dl.fetch_data()
    print(dl.columns)
