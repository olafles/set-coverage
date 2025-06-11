"""This file contains different mutation methods for the Evolutionary Algorithm (EA) implementation as well as for the Simulated Annealing (SA) algorithm."""

from solution import Solution
from validator import Validator
import random


class Mutations:
    @staticmethod
    def repair_solution(solution: Solution, validator: Validator) -> Solution:
        """Add random subsets to the solution until it is valid.

        Args:
            solution (Solution): Solution to repair.
            validator (Validator): Validator to check the solution.

        Returns:
            Solution: A valid solution.
        """
        temp_solution = Solution(list(solution.subsets))
        validator.complex_eval_without_fitness(temp_solution)

        current_subsets = set(temp_solution.subsets)
        all_subsets = set(range(validator._m))
        available = list(all_subsets - current_subsets)

        while not temp_solution.is_correct() and available:
            subset_to_add = random.choice(available)
            temp_solution.subsets.append(subset_to_add)
            available.remove(subset_to_add)
            validator.complex_eval_without_fitness(temp_solution)

        return temp_solution

    @staticmethod
    def add_mutation(solution: Solution, validator: Validator) -> Solution:
        """Adds a random subset to the solution and repairs it if necessary.

        Args:
            solution (Solution): Solution to mutate.
            validator (Validator): Validator to check the solution.

        Returns:
            Solution: A mutated solution.
        """
        current_subsets = set(solution.subsets)
        all_subsets = set(range(validator._m))
        available = list(all_subsets - current_subsets)

        if available:
            subset_to_add = random.choice(available)
            new_subsets = solution.subsets + [subset_to_add]
        else:
            new_subsets = list(solution.subsets)

        new_solution = Solution(new_subsets)
        new_solution = Mutations.repair_solution(new_solution, validator)
        return new_solution

    @staticmethod
    def remove_mutation(solution: Solution, validator: Validator) -> Solution:
        """Deletes a random subset from the solution and repairs it if necessary.

        Args:
            solution (Solution): Solution to mutate.
            validator (Validator): Validator to check the solution.

        Returns:
            Solution: A mutated solution.
        """
        if not solution.subsets:
            return Solution(list(solution.subsets))

        index_to_remove = random.randrange(len(solution.subsets))
        new_subsets = list(solution.subsets)
        del new_subsets[index_to_remove]

        new_solution = Solution(new_subsets)
        new_solution = Mutations.repair_solution(new_solution, validator)
        return new_solution

    @staticmethod
    def swap_mutation(solution: Solution, validator: Validator) -> Solution:
        """Swaps a random subset in the solution with a random one and repairs it if necessary.

        Args:
            solution (Solution): Solution to mutate.
            validator (Validator): Validator to check the solution.

        Returns:
            Solution: A mutated solution.
        """
        if not solution.subsets:
            return Solution(list(solution.subsets))

        current_subsets = set(solution.subsets)
        all_subsets = set(range(validator._m))
        available = list(all_subsets - current_subsets)

        if not available:
            return Solution(list(solution.subsets))

        index_to_remove = random.randrange(len(solution.subsets))
        subset_to_add = random.choice(available)

        new_subsets = list(solution.subsets)
        del new_subsets[index_to_remove]
        new_subsets.append(subset_to_add)

        new_solution = Solution(new_subsets)
        new_solution = Mutations.repair_solution(new_solution, validator)
        return new_solution
