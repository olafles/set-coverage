"""This file contains test case for the Random Solution Generator implementation."""

from DataLoader import DataLoader
from validator import Validator
from random_correct import RandomSolutionGenerator
import time

print("=== Random Solution Generator Test ===")
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
rsg = RandomSolutionGenerator(vd)
start_random = time.time()
rand_sol = rsg.generate_random_solution()
end_random = time.time()
print(f"Time it took to generate: {end_random - start_random:.2f} seconds")
print("Random solution test:")
print(sorted(rand_sol.subsets))
print(len(rand_sol.subsets))
vd.complex_eval_without_fitness(rand_sol)
print(f"Cost: {rand_sol.get_cost_sum()}, Valid: {rand_sol.is_correct()}")
print(f"Fitness: {rand_sol.get_fitness():.4f}")
