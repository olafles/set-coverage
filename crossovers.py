from solution import Solution
from validator import Validator
from mutations import Mutations
import random


class Crossovers:
    @staticmethod
    def uniform_crossover(
        parent1: Solution, parent2: Solution, validator: Validator
    ) -> Solution:
        """Krzyżowanie jednorodne - losowo wybiera podzbiory z rodziców."""
        combined = list(set(parent1.subsets + parent2.subsets))
        child_subsets = []

        # Losowo wybieraj podzbiory z połączonej listy
        for subset in combined:
            if random.random() < 0.5:
                child_subsets.append(subset)

        child = Solution(child_subsets)
        child = Mutations.repair_solution(child, validator)  # Naprawa
        validator.remove_redundant_subsets(child, continuous=True)  # Usuń nadmiarowe
        return child

    @staticmethod
    def greedy_crossover(
        parent1: Solution, parent2: Solution, validator: Validator
    ) -> Solution:
        """Krzyżowanie 'zachłanne' - łączy podzbiory rodziców i optymalizuje."""
        combined = list(set(parent1.subsets + parent2.subsets))
        child = Solution(combined)

        # Usuń nadmiarowe podzbiory i napraw
        validator.remove_redundant_subsets(child, continuous=True)
        if not child.is_correct():
            child = Mutations.repair_solution(child, validator)
        return child

    @staticmethod
    def pmx_crossover(
        parent1: Solution, parent2: Solution, validator: Validator
    ) -> Solution:
        """Zmodyfikowane krzyżowanie PMX dla problemu pokrycia zbioru."""
        # Stwórz sekcję z rodzica1 i uzupełnij brakujące z rodzica2
        cut_start = random.randint(0, len(parent1.subsets) - 1)
        cut_end = random.randint(cut_start, len(parent1.subsets))
        child_subsets = parent1.subsets[cut_start:cut_end]

        # Dodaj unikalne podzbiory z rodzica2
        for subset in parent2.subsets:
            if subset not in child_subsets:
                child_subsets.append(subset)

        child = Solution(child_subsets)
        child = Mutations.repair_solution(child, validator)  # Naprawa
        validator.remove_redundant_subsets(child, continuous=True)
        return child
