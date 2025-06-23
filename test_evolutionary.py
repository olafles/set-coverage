"""This file contains test cases for the Evolutionary Algorithm (EA) implementation."""

from DataLoader import DataLoader
from validator import Validator
from evolutionary import EvolutionaryAlgorithm
import time

print("=== Evolutionary Algorithm Test ===")
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
ea = EvolutionaryAlgorithm(
    validator=vd,
    population_size=500,
    mutation_rate=1.0,  # 0.35 dla swap normalnego, 1.0 dla swap per gen
    crossover_rate=0.0,
    tournament_size=50,
    elitism_count=5,
    crossover_method="pmx",  #  uniform, greedy, pmx
    mutation_method="swap_per_gen",  #  add, remove, swap, remove_per_gen, swap_per_gen
    selection_method="tournament",  #  tournament, roulette
)
start_time = time.time()
gen_size = 500
best_solution, best_history, avg_history = ea.run(
    generations=gen_size, verbose=True, draw=True
)
end_time = time.time()
print(f"Time it took to generate: {end_time - start_time:.2f} seconds")
stats = ea.get_statistics()
print(f"Best fitness: {stats['best_fitness']:.4f}")
print(f"Best cost: {stats['best_cost']}")
print(f"Number of subsets used: {stats['num_subsets']}")
print(f"Subsets selected: {stats['best_subsets']}")