"""This file contains Population Generator class for the Set Cover Problem (SCP) implementation."""

from random_correct import RandomSolutionGenerator
from typing import List
from validator import Validator
from solution import Solution


class PopulationGenerator:
    @staticmethod
    def generate_initial_population(
        pop_size: int, validator: Validator
    ) -> List[Solution]:
        """Generates an initial population of random solutions.

        Args:
            pop_size (int): Size of the population.
            validator (Validator): Validator instance for checking solution validity.

        Returns:
            List[Solution]: List of random solutions.
        """
        generator = RandomSolutionGenerator(validator)
        population = []
        for _ in range(pop_size):
            solution = generator.generate_random_solution()
            population.append(solution)
        return population
