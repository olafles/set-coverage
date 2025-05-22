from random_correct import RandomSolutionGenerator
from typing import List
from validator import Validator
from solution import Solution


class PopulationGenerator:
    @staticmethod
    def generate_initial_population(
        pop_size: int, validator: Validator
    ) -> List[Solution]:
        """Generuje początkową populację poprawnych rozwiązań."""
        generator = RandomSolutionGenerator(validator)
        population = []
        for _ in range(pop_size):
            solution = generator.generate_random_solution()
            population.append(solution)
        return population
