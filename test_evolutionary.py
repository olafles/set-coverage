"""This file contains test cases for the Evolutionary Algorithm (EA) implementation."""

from DataLoader import DataLoader
from validator import Validator
from evolutionary import EvolutionaryAlgorithm, EvolutionaryAlgorithmComparison
import time

# Testing
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)

# Example 1: Testing the Evolutionary Algorithm
print("=== Evolutionary Algorithm Test ===")
ea = EvolutionaryAlgorithm(
    validator=vd,
    population_size=100,
    mutation_rate=0.15,
    crossover_rate=0.8,
    tournament_size=3,
    elitism_count=2,
    crossover_method="pmx",  # User chooses: uniform, greedy, pmx
    mutation_method="swap",  # User chooses: add, remove, swap
    selection_method="roulette",  # User chooses: tournament, roulette
)
start_time = time.time()
gen_size = 100
best_solution, best_history, avg_history = ea.run(
    generations=gen_size, verbose=True, draw=True
)
end_time = time.time()
print(f"Time it took to run: {end_time - start_time:.2f} seconds")
stats = ea.get_statistics()
print(f"Best fitness: {stats['best_fitness']:.4f}")
print(f"Best cost: {stats['best_cost']}")
print(f"Number of subsets used: {stats['num_subsets']}")
print(f"Subsets selected: {stats['best_subsets']}")

# # RUN MULTIPLE TIMES
# for i in range(10):
#     print(
#         f"\nTesting run {i+1} with {ea.crossover_method}-{ea.mutation_method}-{ea.selection_method}"
#     )
#     start_time = time.time()
#     gen_size = 200
#     best_solution, best_history, avg_history = ea.run(
#         generations=gen_size, verbose=True
#     )
#     end_time = time.time()
#     print(f"Time it took to run: {end_time - start_time:.2f} seconds")
#     stats = ea.get_statistics()
#     print(
#         f"\nResults {i+1} with {stats['crossover_method']}-{stats['mutation_method']}-{stats['selection_method']}:"
#     )
#     print(f"Best fitness: {stats['best_fitness']:.4f}")
#     if stats["best_fitness"] < best_fitness:
#         best_fitness = stats["best_fitness"]
#     print(f"Best cost: {stats['best_cost']}")
#     print(f"Number of subsets used: {stats['num_subsets']}")
#     print(f"Subsets selected: {stats['best_subsets']}")
# print(f"\nBest fitness overall: {best_fitness:.4f}")
# print(f"Best solution: {sorted(best_solution.subsets)}")

# # Example 2: Comparing different method combinations
# print("\n" + "=" * 60)
# print("=== Comparing Different Method Combinations ===")

# # Define specific combinations to test
# method_combinations = [
#     {
#         "crossover_method": "uniform",
#         "mutation_method": "swap",
#         "selection_method": "tournament",
#     },
#     {
#         "crossover_method": "greedy",
#         "mutation_method": "add",
#         "selection_method": "tournament",
#     },
#     {
#         "crossover_method": "pmx",
#         "mutation_method": "remove",
#         "selection_method": "roulette",
#     },
#     {
#         "crossover_method": "uniform",
#         "mutation_method": "add",
#         "selection_method": "roulette",
#     },
#     {
#         "crossover_method": "greedy",
#         "mutation_method": "swap",
#         "selection_method": "roulette",
#     },
# ]

# results = {}
# for i, methods in enumerate(method_combinations):
#     print(
#         f"\nTesting combination {i+1}: {methods['crossover_method']}-{methods['mutation_method']}-{methods['selection_method']}"
#     )

#     ea_test = EvolutionaryAlgorithm(validator=vd, population_size=30, **methods)

#     best_sol, _, _ = ea_test.run(generations=75, verbose=False)

#     results[f"combo_{i+1}"] = {
#         "methods": methods,
#         "cost": best_sol.get_cost_sum(),
#         "fitness": best_sol.get_fitness(),
#         "subsets_count": len(best_sol.subsets),
#     }

#     print(
#         f"Result: Cost={best_sol.get_cost_sum()}, Fitness={best_sol.get_fitness():.4f}"
#     )

# # Example 3: Testing all crossover methods with same other parameters
# print("\n" + "=" * 60)
# print("=== Comparing All Crossover Methods ===")

# crossover_methods = ["uniform", "greedy", "pmx"]
# crossover_results = {}

# for crossover in crossover_methods:
#     print(f"\nTesting {crossover} crossover...")

#     ea_cross = EvolutionaryAlgorithm(
#         validator=vd,
#         population_size=30,
#         crossover_method=crossover,
#         mutation_method="swap",  # Keep same
#         selection_method="tournament",  # Keep same
#     )

#     best_sol, _, _ = ea_cross.run(generations=80, verbose=False)
#     crossover_results[crossover] = {
#         "cost": best_sol.get_cost_sum(),
#         "fitness": best_sol.get_fitness(),
#         "subsets_count": len(best_sol.subsets),
#     }

#     print(
#         f"{crossover.capitalize()} crossover: Cost={best_sol.get_cost_sum()}, "
#         f"Fitness={best_sol.get_fitness():.4f}"
#     )

# # Example 4: Testing all mutation methods
# print("\n" + "=" * 60)
# print("=== Comparing All Mutation Methods ===")

# mutation_methods = ["add", "remove", "swap"]
# mutation_results = {}

# for mutation in mutation_methods:
#     print(f"\nTesting {mutation} mutation...")

#     ea_mut = EvolutionaryAlgorithm(
#         validator=vd,
#         population_size=30,
#         crossover_method="uniform",  # Keep same
#         mutation_method=mutation,
#         selection_method="tournament",  # Keep same
#     )

#     best_sol, _, _ = ea_mut.run(generations=80, verbose=False)
#     mutation_results[mutation] = {
#         "cost": best_sol.get_cost_sum(),
#         "fitness": best_sol.get_fitness(),
#         "subsets_count": len(best_sol.subsets),
#     }

#     print(
#         f"{mutation.capitalize()} mutation: Cost={best_sol.get_cost_sum()}, "
#         f"Fitness={best_sol.get_fitness():.4f}"
#     )

# # Example 5: Testing both selection methods
# print("\n" + "=" * 60)
# print("=== Comparing Selection Methods ===")

# selection_methods = ["tournament", "roulette"]
# selection_results = {}

# for selection in selection_methods:
#     print(f"\nTesting {selection} selection...")

#     ea_sel = EvolutionaryAlgorithm(
#         validator=vd,
#         population_size=30,
#         crossover_method="uniform",  # Keep same
#         mutation_method="swap",  # Keep same
#         selection_method=selection,
#     )

#     best_sol, _, _ = ea_sel.run(generations=80, verbose=False)
#     selection_results[selection] = {
#         "cost": best_sol.get_cost_sum(),
#         "fitness": best_sol.get_fitness(),
#         "subsets_count": len(best_sol.subsets),
#     }

#     print(
#         f"{selection.capitalize()} selection: Cost={best_sol.get_cost_sum()}, "
#         f"Fitness={best_sol.get_fitness():.4f}"
#     )

# # Example 6: Dynamic method changing
# print("\n" + "=" * 60)
# print("=== Dynamic Method Changing ===")

# dynamic_ea = EvolutionaryAlgorithm(
#     validator=vd,
#     crossover_method="uniform",
#     mutation_method="add",
#     selection_method="tournament",
# )

# print("First run with uniform-add-tournament:")
# best1, _, _ = dynamic_ea.run(generations=50, verbose=False)
# print(f"Result 1: Cost={best1.get_cost_sum()}, Fitness={best1.get_fitness():.4f}")

# # Change methods
# dynamic_ea.set_parameters(
#     crossover_method="greedy", mutation_method="swap", selection_method="roulette"
# )

# print("\nSecond run with greedy-swap-roulette:")
# best2, _, _ = dynamic_ea.run(generations=50, verbose=False)
# print(f"Result 2: Cost={best2.get_cost_sum()}, Fitness={best2.get_fitness():.4f}")

# # Example 7: Comprehensive method comparison using built-in function
# print("\n" + "=" * 60)
# print("=== Comprehensive Method Comparison ===")
# print("Testing all 18 possible combinations (this may take a moment)...")

# comprehensive_results = EvolutionaryAlgorithmComparison.compare_methods(
#     validator=vd,
#     generations=60,
#     runs_per_method=2,  # Reduced for faster execution
# )

# # Find best combination
# best_combination = min(
#     comprehensive_results.items(), key=lambda x: x[1]["best_fitness"]
# )

# print(f"\nBest combination found:")
# print(
#     f"Methods: {best_combination[1]['crossover']}-{best_combination[1]['mutation']}-{best_combination[1]['selection']}"
# )
# print(f"Best fitness: {best_combination[1]['best_fitness']:.4f}")
# print(f"Best cost: {best_combination[1]['best_cost']}")
# print(f"Average fitness: {best_combination[1]['avg_fitness']:.4f}")

# # Print top 3 combinations
# print(f"\nTop 3 combinations:")
# sorted_results = sorted(
#     comprehensive_results.items(), key=lambda x: x[1]["best_fitness"]
# )

# for i, (name, result) in enumerate(sorted_results[:3]):
#     print(
#         f"{i+1}. {result['crossover']}-{result['mutation']}-{result['selection']}: "
#         f"Best={result['best_fitness']:.4f}, Avg={result['avg_fitness']:.4f}"
#     )
