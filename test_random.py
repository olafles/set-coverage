"""This file contains test case for the Random Solution Generator implementation."""

from DataLoader import DataLoader
from validator import Validator
from random_correct import RandomSolutionGenerator

# Testing Random Solution Generator
print("=== Random Solution Generator Test ===")
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
rsg = RandomSolutionGenerator(vd)
rand_sol = rsg.generate_random_solution()
print("Random solution test:")
print(sorted(rand_sol.subsets))
print(len(rand_sol.subsets))
vd.complex_eval(rand_sol)
print("Original Solution:")
print(
    f"Subsets: {rand_sol.subsets}, Cost: {rand_sol.get_cost_sum()}, Valid: {rand_sol.is_correct()}"
)
print(f"Fitness: {rand_sol.get_fitness():.4f}")
