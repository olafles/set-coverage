"""This file contains test cases for the Simulated Annealing (SA) implementation."""

from DataLoader import DataLoader
from validator import Validator
from sa import SimulatedAnnealing
import time

# Testing
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
sa = SimulatedAnnealing(vd)
start_time = time.time()

# test_sa = sa.run(1000, 0.01, 0.1e-5, 10_000, draw=True)  # Default
# test_sa = sa.run(5000, 0.005, 0.1e-6, 20_000)  # Slow cooling more exploration
# test_sa = sa.run(500, 0.05, 0.1e-3, 5_000)  # Agressive cooling
# test_sa = sa.run(10_000, 0.02, 0.1e-7, 15_000)  # High T start
# test_sa = sa.run(2000, 0.001, 0.1e-8, 50_000, draw=True)  # Long run
test_sa = sa.run(draw=True, max_iterations=2000)
end_time = time.time()
print(f"Time it took to run: {end_time - start_time:.2f} seconds")
