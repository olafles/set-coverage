"""This file contains test case for the Simulated Annealing (SA) implementation."""

from DataLoader import DataLoader
from validator import Validator
from simulated_annealing import SimulatedAnnealing
import time

# Testing Simulated Annealing
print("=== Simulated Annealing Test ===")
dl = DataLoader("scp41.txt")
dl.fetch_data()
vd = Validator(dl)
sa = SimulatedAnnealing(vd)
start_time = time.time()

test_sa = sa.run(
    initial_temp=2000.0,
    min_temp=0.000001,
    cooling_rate=0.9995,
    cooling_strategy="exponential",  # "linear", "exponential", "logarithmic"
    max_iterations=100000,
    debug=True,
    draw=True,
)
end_time = time.time()
print(f"Time it took to run: {end_time - start_time:.2f} seconds")
print(f"Best solution: {sorted(test_sa.subsets)}")
print(f"\nNajlepsze rozwiązanie: {len(test_sa.subsets)} podzbiorów")
print(f"Najlepszy fitness: {test_sa.get_fitness():.6f}")
print(f"Pokrycie: {'OK' if test_sa.is_correct() else 'Niekompletne'}")
