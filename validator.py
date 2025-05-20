from solution import Solution
from typing import List
from DataLoader import DataLoader


class Validator:
    def __init__(self, dl: DataLoader) -> None:
        """Subclass for simulation used for calculating various things

        Args:
            n (int): Number of elements that need to be covered
            m (int): Number of subsets that can be choosen
            costs (List[int]): Costs of subsets
            covers (List[List[int]]): Elements covered by each subset
        """
        self._n = dl.get_n()
        self._m = dl.get_m()
        self._costs = dl.get_costs()
        self._covers = dl.get_subset_covers()
        self._all_elements = set(range(self._n))
        pass

    def calculate_covered_elements(self, solution: Solution) -> list[int]:
        """Calculate elements covered by a solution

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            List[int]: List of covered elements
        """
        covered_elements = set()
        # print(f"{len(self._covers)=}")
        for subset in solution.subsets:
            # print(subset)
            covered_elements.update(self._covers[subset])
            # print(covered_elements)
        sorted_covered = sorted(covered_elements)
        solution._covered_elements = sorted_covered
        return sorted_covered

    def is_correct(self, solution: Solution) -> bool:
        """Check if solution covers all elements

        Args:
            solution (Solution): Solution object to check

        Returns:
            bool: True if all elements are covered
        """
        covered = self.calculate_covered_elements(solution)
        # print(f"{covered=}")
        if set(covered) == self._all_elements:
            solution._is_correct = True
            return True
        return False

    def sum_costs(self, solution: Solution) -> int:
        """Calculate sum of subsets' costs from a solution

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            int: Sum of costs
        """
        sum_of_costs = sum(self._costs[subset] for subset in solution.subsets)
        solution._cost_sum = sum_of_costs
        return sum_of_costs

    def calculate_fitness(self, solution: Solution) -> float:
        """Calculate solutions fitness based on covered elements and cost

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            float: Fitness indicator
        """
        fitness = len(solution.subsets) / self.sum_costs(solution)
        solution._fitness = fitness
        return fitness

    def complex_eval(self, solution: Solution) -> None:
        # TODO Combine all above
        pass
