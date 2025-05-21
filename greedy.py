from validator import Validator
from solution import Solution
from typing import Set, List
import time


class GreedySolutionGenerator:
    def __init__(self, validator: Validator) -> None:
        self.validator = validator

    def _generate_greedy_solution(self, start_subset: int = None) -> Solution:
        """Generates a greedy solution, selecting subsets with the best ratio of new elements to cost."""
        n = self.validator._n
        costs = self.validator._costs
        covers = self.validator._covers

        all_elements = set(range(n))
        covered: Set[int] = set()
        available_subsets = set(range(self.validator._m))
        solution_subsets = []

        if start_subset is not None and start_subset in available_subsets:
            solution_subsets.append(start_subset)
            covered.update(covers[start_subset])
            available_subsets.remove(start_subset)

        while covered < all_elements:
            best_subset = None
            best_value = -float("inf")

            for subset in available_subsets:
                new_elements = set(covers[subset]) - covered
                new_count = len(new_elements)
                if new_count == 0:
                    continue  # Skip subsets that don't add new elements

                ratio = new_count / (costs[subset] + 0.1 * len(solution_subsets))
                if ratio > best_value:
                    best_value = ratio
                    best_subset = subset

            if best_subset is None:
                break  # No more subsets to add

            solution_subsets.append(best_subset)
            covered.update(covers[best_subset])
            available_subsets.remove(best_subset)

        solution = Solution(solution_subsets)
        self.validator.is_correct(solution)
        self.validator.sum_costs(solution)
        self.validator.calculate_fitness(solution)
        return solution

    def generate_population(self) -> List[Solution]:
        """Generates m solutions each starting from a different subset."""
        solutions = []
        start_time = time.time()
        for start_subset in range(self.validator._m):
            print(start_subset)
            try:
                solution = self._generate_greedy_solution(start_subset)
                if solution.is_correct():
                    solutions.append(solution)
            except:
                continue
        end_time = time.time()
        elapsed_time = end_time - start_time
        print(f"Time it took to generate: {elapsed_time:.2f} seconds")
        return solutions

    def get_best_solution(self, solutions: List[Solution]) -> Solution:
        """Returns the best solution from a list of solutions."""
        if not solutions:
            raise ValueError("No valid solutions found.")
        return max(solutions, key=lambda sol: sol.get_fitness())
