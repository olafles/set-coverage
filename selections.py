"""This file contains different selection methods for the Evolutionary Algorithm (EA) implementation."""

from solution import Solution
from typing import List
import random


class Selection:
    @staticmethod
    def tournament_selection(
        population: List[Solution], num_parents: int, tournament_size: int = 3
    ) -> List[Solution]:
        """Tournament selection - selects the best solution from a random subset of the population.

        Args:
            population (List[Solution]): List of solutions to select from.
            num_parents (int): Number of parents to select.
            tournament_size (int): Number of participants in each tournament.

        Returns:
            List[Solution]: Selected parents.
        """
        selected = []
        for _ in range(num_parents):
            participants = random.sample(population, tournament_size)
            best = min(participants, key=lambda sol: sol.get_fitness())
            selected.append(best)
        return selected

    @staticmethod
    def roulette_selection(
        population: List[Solution], num_parents: int
    ) -> List[Solution]:
        """Roulette selection - selection probability proportional to 1/fitness.

        Args:
            population (List[Solution]): List of solutions to select from.
            num_parents (int): Number of parents to select.

        Returns:
            List[Solution]: Selected parents.
        """
        fitness_values = [
            1 / (sol.get_fitness() + 1e-6) for sol in population
        ]  # +1e-6 aby uniknąć dzielenia przez 0
        total = sum(fitness_values)
        probabilities = [f / total for f in fitness_values]

        return random.choices(population, weights=probabilities, k=num_parents)
