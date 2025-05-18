from typing import List
from validator import Validator


class Solution:
    subsets = []
    is_correct = False
    cost_sum = 0
    fitness = 0  # Albo inf zależy od podejscia
    covered_elements = []

    def __init__(self, input_subsets: List[int], validator: Validator) -> None:
        if input_subsets is None or len(input_subsets) == 0:
            raise Exception("Input subsets list is None")
        self.subsets = input_subsets
        # TODO self.is_correct = validate(self.subsets)
        # Opcjonalnie if not self.is_correct raise Exception
        # TODO self.cost_sum = cost(self.subsets)
        # TODO self.fitness = fitness(self.subsets)
