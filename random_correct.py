"""This file contains RandomSolutionGenerator class for the Set Cover Problem (SCP) implementation."""

import random
from DataLoader import DataLoader
from validator import Validator
from solution import Solution


class RandomSolutionGenerator:
    def __init__(self, validator: Validator) -> None:
        self.validator = validator
        pass

    def generate_random_solution(self) -> Solution:
        """Generate a random solution for the Set Cover Problem.

        Returns:
            Solution: A random solution that covers all elements.
        """
        all_subsets = list(range(0, self.validator._m))
        random.shuffle(all_subsets)
        solution = Solution(
            [all_subsets.pop(all_subsets.index(random.choice(all_subsets)))]
        )
        while not solution._is_correct:
            solution.subsets.append(
                all_subsets.pop(all_subsets.index(random.choice(all_subsets)))
            )
            self.validator.is_correct(solution)
        self.validator.complex_eval(solution)
        return solution


if __name__ == "__main__":
    dl = DataLoader("scp_toy.txt")
    dl.fetch_data()
    validator = Validator(dl)
    print(dl.get_m())
    rsg = RandomSolutionGenerator(validator)
    solution = rsg.generate_random_solution()
    print(len(solution.subsets))
