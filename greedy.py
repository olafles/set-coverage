from validator import Validator
from solution import Solution
from typing import Set, List
import time


class GreedySolutionGenerator:
    def __init__(self, validator: Validator) -> None:
        self.validator = validator

    def _generate_greedy_solution(self, start_subset: int = None) -> Solution:
        """Generuje rozwiązanie, wybierając podzbiory o najwyższym stosunku nowych elementów do kosztu."""
        n = self.validator._n
        costs = self.validator._costs
        covers = self.validator._covers

        all_elements = set(range(n))
        covered: Set[int] = set()
        available_subsets = set(range(self.validator._m))
        solution_subsets = []

        # Startuj od konkretnego subsetu (jeśli podano)
        if start_subset is not None and start_subset in available_subsets:
            solution_subsets.append(start_subset)
            covered.update(covers[start_subset])
            available_subsets.remove(start_subset)

        # Główna pętla zachłanna
        while covered < all_elements:
            best_subset = None
            best_value = -float("inf")

            for subset in available_subsets:
                new_elements = set(covers[subset]) - covered
                new_count = len(new_elements)
                if new_count == 0:
                    continue  # Pomijaj podzbiory bez nowych elementów

                # Nowa metryka: (nowe elementy) / (koszt + kary za rozmiar)
                ratio = new_count / (costs[subset] + 0.1 * len(solution_subsets))
                if ratio > best_value:
                    best_value = ratio
                    best_subset = subset

            if best_subset is None:
                break  # Brak użytecznych podzbiorów

            solution_subsets.append(best_subset)
            covered.update(covers[best_subset])
            available_subsets.remove(best_subset)

        solution = Solution(solution_subsets)
        self.validator.is_correct(solution)
        self.validator.sum_costs(solution)
        self.validator.calculate_fitness(solution)
        return solution

    def generate_population(self) -> List[Solution]:
        """Generuje m rozwiązań, każde startujące od innego subsetu."""
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
        print(f"Czas generowania populacji: {elapsed_time:.2f} sekund")
        return solutions

    def get_best_solution(self, solutions: List[Solution]) -> Solution:
        """Zwraca rozwiązanie z najwyższym fitness."""
        if not solutions:
            raise ValueError("Brak poprawnych rozwiązań.")
        return max(solutions, key=lambda sol: sol.get_fitness())
