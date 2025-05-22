"""This file contains crossover methods for the Evolutionary Algorithm (EA) implementation."""

from solution import Solution
from validator import Validator
from mutations import Mutations
import random


class Crossovers:
    @staticmethod
    def uniform_crossover(
        parent1: Solution, parent2: Solution, validator: Validator
    ) -> Solution:
        """Uniform crossover - randomly selects subsets from both parents.

        Args:
            parent1 (Solution): First parent solution.
            parent2 (Solution): Second parent solution.
            validator (Validator): Validator to check the solution.

        Returns:
            Solution: A new solution created from the parents.
        """
        combined = list(set(parent1.subsets + parent2.subsets))
        child_subsets = []

        for subset in combined:
            if random.random() < 0.5:
                child_subsets.append(subset)

        child = Solution(child_subsets)
        child = Mutations.repair_solution(child, validator)
        validator.remove_redundant_subsets(child, continuous=True)
        return child

    @staticmethod
    def greedy_crossover(
        parent1: Solution, parent2: Solution, validator: Validator
    ) -> Solution:
        """Greedy crossover - combines subsets from both parents and optimizes them.

        Args:
            parent1 (Solution): First parent solution.
            parent2 (Solution): Second parent solution.
            validator (Validator): Validator to check the solution.
        Returns:
            Solution: A new solution created from the parents.
        """
        combined = list(set(parent1.subsets + parent2.subsets))
        child = Solution(combined)

        validator.remove_redundant_subsets(child, continuous=True)
        if not child.is_correct():
            child = Mutations.repair_solution(child, validator)
        return child

    @staticmethod
    def pmx_crossover(
        parent1: Solution, parent2: Solution, validator: Validator
    ) -> Solution:
        """Modified PMX crossover - combines subsets from both parents for Set Cover Problem.

        Args:
            parent1 (Solution): First parent solution.
            parent2 (Solution): Second parent solution.
            validator (Validator): Validator to check the solution.
        Returns:
            Solution: A new solution created from the parents.
        """
        cut_start = random.randint(0, len(parent1.subsets) - 1)
        cut_end = random.randint(cut_start, len(parent1.subsets))
        child_subsets = parent1.subsets[cut_start:cut_end]

        for subset in parent2.subsets:
            if subset not in child_subsets:
                child_subsets.append(subset)

        child = Solution(child_subsets)
        child = Mutations.repair_solution(child, validator)
        validator.remove_redundant_subsets(child, continuous=True)
        return child
