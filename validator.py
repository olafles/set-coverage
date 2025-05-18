class Validator:
    def __init__(self, n, m, costs, covers):
        """Subclass for simulation used for calculating various things

        Args:
            n (int): Number of elements that need to be covered
            m (int): Number of subsets that can be choosen
            costs (List[int]): Costs of subsets
            covers (List[List[int]]): Elements covered by each subset
        """
        self._n = n
        self._m = m
        self._costs = costs
        self._covers = covers
        self._all_elements = set(range(1, n + 1))
        pass

    def calculate_covered_elements(self, solution) -> list[int]:
        """Calculate elements covered by a solution

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            List[int]: List of covered elements
        """
        covered_elements = set()
        for subset in solution.subsets:
            covered_elements.update(self._covers[subset])
        return sorted(covered_elements)

    def is_correct(self, solution) -> bool:
        """Check if solution covers all elements

        Args:
            solution (Solution): Solution object to check

        Returns:
            bool: True if all elements are covered
        """
        covered = self.calculate_covered_elements(solution)
        return set(covered) == self._all_elements

    def sum_costs(self, solution) -> int:
        """Calculate sum of subsets' costs from a solution

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            int: Sum of costs
        """
        return sum(self._costs[subset] for subset in solution.subsets)

    def calculate_fitness(self, solution) -> float:
        """Calculate solutions fitness based on covered elements and cost

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            float: Fitness indicator
        """
        if self.is_correct(solution):
            return self.sum_costs(solution)
        return float("inf")
