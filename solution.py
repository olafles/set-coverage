from typing import List


class Solution:

    def __init__(self, input_subsets: List[int]) -> None:
        self.subsets = input_subsets
        self._is_correct = False
        self._cost_sum = 0
        self._fitness = float("inf")  # Albo inf zależy od podejscia
        self._covered_elements = []

    def get_cost_sum(self) -> int:
        return self._cost_sum

    def is_correct(self) -> bool:
        return self._is_correct

    def get_fitness(self) -> float:
        return self._fitness

    def get_covered_elements(self) -> list[int]:
        return self._covered_elements
