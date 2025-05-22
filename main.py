from DataLoader import DataLoader
from solution import Solution
from validator import Validator
from random_correct import RandomSolutionGenerator
from greedy import GreedySolutionGenerator
from mutations import Mutations
from crossovers import Crossovers
from evolutionary import EvolutionaryAlgorithm, EvolutionaryAlgorithmComparison
import time
import matplotlib.pyplot as plt
from visualiser import EA_Graph

# Testing
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
# Example 1: Testing the Evolutionary Algorithm
print("=== Basic EA with User-Defined Methods ===")
ea = EvolutionaryAlgorithm(
    validator=vd,
    population_size=500,
    mutation_rate=0.15,
    crossover_rate=0.8,
    tournament_size=3,
    elitism_count=2,
    crossover_method="pmx",  # User chooses: uniform, greedy, pmx
    mutation_method="swap",  # User chooses: add, remove, swap
    selection_method="roulette",  # User chooses: tournament, roulette
)
best_fitness = float("inf")
for i in range(10):
    print(
        f"\nTesting run {i+1} with {ea.crossover_method}-{ea.mutation_method}-{ea.selection_method}"
    )
    start_time = time.time()
    gen_size = 200
    best_solution, best_history, avg_history = ea.run(
        generations=gen_size, verbose=True
    )
    end_time = time.time()
    print(f"Time it took to run: {end_time - start_time:.2f} seconds")
    stats = ea.get_statistics()
    print(
        f"\nResults {i+1} with {stats['crossover_method']}-{stats['mutation_method']}-{stats['selection_method']}:"
    )
    print(f"Best fitness: {stats['best_fitness']:.4f}")
    if stats["best_fitness"] < best_fitness:
        best_fitness = stats["best_fitness"]
    print(f"Best cost: {stats['best_cost']}")
    print(f"Number of subsets used: {stats['num_subsets']}")
    print(f"Subsets selected: {stats['best_subsets']}")
print(f"\nBest fitness overall: {best_fitness:.4f}")
print(f"Best solution: {sorted(best_solution.subsets)}")
