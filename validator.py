"""This file contains Validator class for the Set Cover Problem (SCP) implementation."""

from solution import Solution
from typing import List
from DataLoader import DataLoader
import math


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

        # Calculate gamma for instance
        max_cost_per_element = 0
        for j in range(len(self._covers)):
            subset_size = len(self._covers[j])
            if subset_size == 0:
                continue  # Avoid division by zero (invalid subset)
            cost_per_element = self._costs[j] / subset_size
            if cost_per_element > max_cost_per_element:
                max_cost_per_element = cost_per_element

        self._gamma = 10  # max(math.ceil(max_cost_per_element), 1)  # Gamma ≥ 1
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

    def calculate_fitness_old(self, solution: Solution) -> float:
        """Calculate solutions fitness based on covered elements and cost

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            float: Fitness indicator
        """
        if not self.is_correct(solution):
            return float("inf")

        cost_weight = 0.5
        subsets_weight = 0.5

        normalized_cost = self.sum_costs(solution) / sum(self._costs)
        normalized_subsets = len(solution.subsets) / self._m

        fitness = (cost_weight * normalized_cost) + (
            subsets_weight * normalized_subsets
        )
        solution._fitness = fitness
        return fitness

    def complex_eval_without_fitness(self, solution: Solution) -> None:
        """Check if solution is correct and calculate the cost

        Args:
            solution (Solution): Solution to evaluate
        """
        self.is_correct(solution)
        self.sum_costs(solution)
        pass

    def complex_eval(self, solution: Solution) -> None:
        """Evaluate a solution and set all values in the solution object,
        This function is a combination of all the above functions.

        Args:
            solution (Solution): Solution to evaluate
        """
        self.is_correct(solution)
        self.sum_costs(solution)
        self.calculate_fitness(solution)
        pass

    def remove_redundant_subsets(
        self, solution: Solution, reverse: bool = False, continuous: bool = False
    ) -> bool:
        """Remove redundant subsets from the solution while maintaining full coverage.

        Args:
            solution (Solution): Solution to optimize
            reverse (bool): If True, checks subsets from back to front. Default False.
            continuous (bool): If True, checks all subsets and removes all redundant ones. Default False.

        Returns:
            bool: True if any redundant subset was found and removed, False otherwise
        """
        # if not solution.subsets:          # This might make no sense
        #     return False

        # Get current covered elements
        current_covered = set(self.calculate_covered_elements(solution))
        removed_any = False
        subset_indices = range(len(solution.subsets))

        # Reverse the order if needed
        if reverse:
            subset_indices = reversed(subset_indices)

        # Create a copy of indices to avoid modifying while iterating
        indices_to_check = list(subset_indices)

        for i in indices_to_check:
            # Skip if this subset was already removed in continuous mode
            if i >= len(solution.subsets):
                continue

            # Calculate coverage without this subset
            temp_subsets = solution.subsets[:i] + solution.subsets[i + 1 :]
            temp_solution = Solution(temp_subsets)
            temp_covered = set(self.calculate_covered_elements(temp_solution))

            # If coverage is still complete, remove the subset
            if temp_covered == current_covered:
                solution.subsets.pop(i)
                removed_any = True

                # If not in continuous mode, return after first removal
                if not continuous:
                    break

        if removed_any:
            self.complex_eval_without_fitness(solution)
        return removed_any

    def remove_redundant_subsets_for_greedy(
        self, solution: Solution, reverse: bool = False, continuous: bool = False
    ) -> bool:
        """Remove redundant subsets from the solution while maintaining full coverage.

        Args:
            solution (Solution): Solution to optimize
            reverse (bool): If True, checks subsets from back to front. Default False.
            continuous (bool): If True, checks all subsets and removes all redundant ones. Default False.

        Returns:
            bool: True if any redundant subset was found and removed, False otherwise
        """
        # if not solution.subsets:          # This might make no sense
        #     return False

        # Get current covered elements
        current_covered = set(self.calculate_covered_elements(solution))
        removed_any = False
        subset_indices = range(len(solution.subsets))

        # Reverse the order if needed
        if reverse:
            subset_indices = reversed(subset_indices)

        # Create a copy of indices to avoid modifying while iterating
        indices_to_check = list(subset_indices)

        for i in indices_to_check:
            # Skip if this subset was already removed in continuous mode
            if i >= len(solution.subsets):
                continue

            # Calculate coverage without this subset
            temp_subsets = solution.subsets[:i] + solution.subsets[i + 1 :]
            temp_solution = Solution(temp_subsets)
            temp_covered = set(self.calculate_covered_elements(temp_solution))

            # If coverage is still complete, remove the subset
            if temp_covered == current_covered:
                solution.subsets.pop(i)
                removed_any = True

                # If not in continuous mode, return after first removal
                if not continuous:
                    break

        if removed_any:
            self.complex_eval(solution)
        return removed_any

    def calculate_fitness(
        self,
        solution: Solution,
        conflict_threshold_k: int = 1,
    ):
        """
        Calculate solution cost based on conflict graph

        Args:
            solution (list): Indices of selected subsets (e.g., [5, 3, 0, 1]).
            conflict_threshold_k (int): Maximum allowed overlap without penalty.

        Returns:
            Total cost (float): Sum of subset costs + conflict penalties.
        """

        # Check if solution is valid (covers all elements)
        if not self.is_correct(solution):
            # print("Incorrect solution had its fitness calculated...")
            return float(999999)
        # print("Correct solution had its fitness calculated...")

        # Calculate total cost and penalties for VALID solutions
        total_cost = sum(self._costs[j] for j in solution.subsets)

        for i in range(len(solution.subsets)):
            subset_i = self._covers[solution.subsets[i]]
            for j in range(i + 1, len(solution.subsets)):
                subset_j = self._covers[solution.subsets[j]]
                overlap = len(set(subset_i) & set(subset_j))
                if overlap > conflict_threshold_k:
                    total_cost += self._gamma * (overlap - conflict_threshold_k)
        solution._fitness = total_cost
        return total_cost
