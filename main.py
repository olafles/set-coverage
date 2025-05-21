from DataLoader import DataLoader
from validator import Validator
from random_correct import RandomSolutionGenerator
from greedy import GreedySolutionGenerator

# Testing
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
rsg = RandomSolutionGenerator(vd)
test_sol = rsg.generate_random_solution()
print("Random solution test:")
print(sorted(test_sol.subsets))
print(len(test_sol.subsets))
print("Greedy solution test:")
gsg = GreedySolutionGenerator(vd)
population = gsg.generate_population()
if population:
    best_solution = gsg.get_best_solution(population)
    print("Subset-y:", sorted(best_solution.subsets))
    print("Ilosc subsetow:", len(best_solution.subsets))
    print("Koszt:", best_solution.get_cost_sum())
    print("Fitness:", best_solution.get_fitness())
else:
    print("Nie znaleziono żadnych poprawnych rozwiązań.")
