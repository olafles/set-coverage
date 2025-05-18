import random
from DataLoader import DataLoader
from validator import Validator
from solution import Solution
from typing import List


class RandomSolutionGenerator:
    def __init__(self, validator: Validator) -> None:
        self.validator = validator
        pass

    def generate_random_solution(self) -> Solution:
        all_subsets = list(range(1, self.validator._m))
        random.shuffle(all_subsets)

        selected_subsets = []
        covered_elements = set()
        for subset in all_subsets:
            selected_subsets.append(subset)
            covered = self.validator.calculate_covered_elements(
                Solution(selected_subsets, self.validator)
            )
            if self.validator.is_correct(Solution(selected_subsets, self.validator)):
                break
        return Solution(selected_subsets, self.validator)
        # TODO Fix this (co tu sie dzieje)

    def generate_multiple_random_solutions(self, count: int) -> List[Solution]:
        """Generate multiple random solutions"""
        return [self.generate_random_solution() for _ in range(count)]


if __name__ == "__main__":
    # Example usage
    dl = DataLoader("scp_toy.txt")
    dl.fetch_data()
    validator = Validator(
        dl.get_n() - 1, dl.get_m() - 1, dl.get_costs(), dl.get_subset_covers()
    )
    rsg = RandomSolutionGenerator(validator)

    print("Generating random solutions until full coverage:")
    for i, solution in enumerate(rsg.generate_multiple_random_solutions(5)):
        print(f"Solution {i+1}: Subsets: {solution.subsets}")
        print(
            f"Covered elements: {len(validator.calculate_covered_elements(solution))}/{validator._n}"
        )
        print(f"Is correct: {validator.is_correct(solution)}")
        print(f"Cost: {validator.sum_costs(solution)}")
        print()
