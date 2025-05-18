from typing import List
from validator import Validator


class Solution:
    subsets = []
    _is_correct = False
    _cost_sum = 0
    _fitness = 0  # Albo inf zależy od podejscia
    _covered_elements = []

    def __init__(self, input_subsets: List[int], validator: Validator) -> None:
        self._validator = validator
        if input_subsets is None or len(input_subsets) == 0:
            raise Exception("Input subsets list is None")
        self.subsets = input_subsets
        # TODO self.is_correct = validate(self.subsets)
        # Opcjonalnie if not self.is_correct raise Exception
        # TODO self.cost_sum = cost(self.subsets)
        # TODO self.fitness = fitness(self.subsets)

    def recalc(self) -> None:
        """Re-run correctness and ranking calculations

        Raises:
            Exception: Subsets list is empty or None
        """
        if self.subsets is None or len(self.subsets) == 0:
            raise Exception("Solutions subsets attribute list is None")
        # TODO self.is_correct = validate(self.subsets)
        # TODO self.cost_sum = cost(self.subsets)
        if self._is_correct:
            # TODO self.fitness = fitness(self.subsets)
            # TODO self._covered_elements = validator.calculate_covered_elements
            pass

    def get_cost_sum(self) -> int:
        return self._cost_sum

    def is_correct(self) -> bool:
        return self._is_correct

    def get_fitness(self) -> float:
        return self._fitness

    def get_covered_elements(self) -> list[int]:
        return self._covered_elements
