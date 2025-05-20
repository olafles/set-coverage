from typing import List


class Solution:
    subsets = []
    _is_correct = False
    _cost_sum = 0
    _fitness = float("inf")  # Albo inf zależy od podejscia
    _covered_elements = []

    def __init__(self, input_subsets: List[int]) -> None:
        self.subsets = input_subsets

    def get_cost_sum(self) -> int:
        return self._cost_sum

    def is_correct(self) -> bool:
        return self._is_correct

    def get_fitness(self) -> float:
        return self._fitness

    def get_covered_elements(self) -> list[int]:
        return self._covered_elements
