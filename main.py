from DataLoader import DataLoader
from validator import Validator
from random_correct import RandomSolutionGenerator

# Testing
dl = DataLoader("scp_toy.txt")
dl.fetch_data()
vd = Validator(dl)
rsg = RandomSolutionGenerator(vd)
test_sol = rsg.generate_random_solution()
print(sorted(test_sol.subsets))
print(len(test_sol.subsets))
