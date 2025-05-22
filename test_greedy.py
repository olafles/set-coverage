"""This file contains test case for the Greedy Solution Generator implementation."""

from DataLoader import DataLoader
from validator import Validator
from greedy import GreedySolutionGenerator
import time

# Testing
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
print("Greedy solution test:")
start_greedy = time.time()
gsg = GreedySolutionGenerator(vd)
population = gsg.generate_population()
end_greedy = time.time()
if population:
    best_solution = gsg.get_best_solution(population)
    print("Subsets selected:", sorted(best_solution.subsets))
    print("Amount of subsets:", len(best_solution.subsets))
    print("Cost:", best_solution.get_cost_sum())
    print(f"Fitness: {best_solution.get_fitness():.4f}")
    print("Time it took to run:", end_greedy - start_greedy)
else:
    print("No valid solutions found.")
