from validator import Validator
from DataLoader import DataLoader
from population import PopulationGenerator
from selections import Selection
from mutations import Mutations

dl = DataLoader("scp_toy.txt")
dl.fetch_data()
vd = Validator(dl)
POP_SIZE = 100
selection_type = "tournament"  # "tournament", "roulette"
mutation_type = "add"  # "add", "remove", "swap"

population = PopulationGenerator.generate_initial_population(POP_SIZE, vd)
print(f"Initial population: {len(population)} solutions")

if selection_type == "tournament":
    parents_selection = Selection.tournament_selection(population, 2)
elif selection_type == "roulette":
    parents_selection = Selection.roulette_selection(population, 2)

for p in parents_selection:
    print(
        f"Parent: {sorted(p.subsets)}, Cost: {p.get_cost_sum()}, Fitness: {p.get_fitness()},  Valid: {p.is_correct()}"
    )

if mutation_type == "add":
    mutation = Mutations.add_mutation(parents_selection[0], vd)
elif mutation_type == "remove":
    mutation = Mutations.remove_mutation(parents_selection[0], vd)
elif mutation_type == "swap":
    mutation = Mutations.swap_mutation(parents_selection[0], vd)

print(
    f"Mutation: {mutation.subsets}, Cost: {mutation.get_cost_sum()}, Fitness: {mutation.get_fitness()},  Valid: {mutation.is_correct()}"
)
