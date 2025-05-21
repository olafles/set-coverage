from DataLoader import DataLoader
from solution import Solution
from validator import Validator
from random_correct import RandomSolutionGenerator
from greedy import GreedySolutionGenerator
from mutations import Mutations
from crossovers import Crossovers

# Testing
dl = DataLoader("scp_toy.txt")
dl.fetch_data()
vd = Validator(dl)
rsg = RandomSolutionGenerator(vd)
test_sol = rsg.generate_random_solution()
# print("Random solution test:")
# print(sorted(test_sol.subsets))
# print(len(test_sol.subsets))
# print("Greedy solution test:")
# gsg = GreedySolutionGenerator(vd)
# population = gsg.generate_population()
# if population:
#     best_solution = gsg.get_best_solution(population)
#     print("Subsets selected:", sorted(best_solution.subsets))
#     print("Amount of subsets:", len(best_solution.subsets))
#     print("Cost:", best_solution.get_cost_sum())
#     print("Fitness:", best_solution.get_fitness())
# else:
#     print("No valid solutions found.")
# Original solution
# original_solution = Solution([0, 1])
vd.complex_eval(test_sol)
print("Original Solution:")
print(
    f"Subsets: {test_sol.subsets}, Cost: {test_sol.get_cost_sum()}, Valid: {test_sol.is_correct()}"
)
print(f"Fitness: {test_sol.get_fitness()}")
