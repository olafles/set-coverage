# [Plik: sa_scp.py]
from validator import Validator
from DataLoader import DataLoader
from solution import Solution
from mutations import Mutations
from random_correct import RandomSolutionGenerator
import random
import math
from typing import Optional
import matplotlib.pyplot as plt


class EnhancedSA:
    def __init__(self, validator: Validator) -> None:
        self.validator = validator
        self.rsg = RandomSolutionGenerator(validator)
        self.history = {
            "iterations": [],
            "temperatures": [],
            "current_costs": [],
            "best_costs": [],
        }

    def run(
        self,
        initial_temp: float = 1000.0,
        min_temp: float = 0.000001,
        cooling_rate: float = 0.999,
        max_iterations: int = 100000,
        debug: bool = False,
    ) -> Solution:
        current = self.rsg.generate_random_solution()
        self.validator.complex_eval(current)
        best = Solution(current.subsets.copy())

        temperature = initial_temp
        iteration = 0

        while temperature > min_temp and iteration < max_iterations:
            neighbor = self._generate_neighbor(current)

            delta = neighbor.get_fitness() - current.get_fitness()

            if self._accept_solution(delta, temperature, neighbor):
                current = neighbor
                if current.get_fitness() < best.get_fitness():
                    best = Solution(current.subsets.copy())
                    self.validator.complex_eval(best)
            if debug:
                print(
                    f"Iter: {iteration}, Temp: {temperature:.2f}, Best: {best.get_fitness():.2f}"
                )

            temperature *= cooling_rate
            iteration += 1

            self._update_history(iteration, temperature, current, best)

        self._plot_progress()
        return best

    def _generate_neighbor(self, solution: Solution) -> Solution:
        mutation_type = random.choices(
            ["add", "remove", "swap", "optimize"], weights=[0.1, 0.5, 0.3, 0.1], k=1
        )[0]

        if mutation_type == "add":
            neighbor = Mutations.add_mutation(solution, self.validator)
        elif mutation_type == "remove":
            neighbor = Mutations.remove_mutation(solution, self.validator)
        elif mutation_type == "swap":
            neighbor = Mutations.swap_mutation(solution, self.validator)
        else:
            neighbor = Solution(solution.subsets.copy())
            self.validator.remove_redundant_subsets(neighbor, continuous=True)

        if not neighbor.is_correct():
            neighbor = Mutations.repair_solution(neighbor, self.validator)
        return neighbor

    def _accept_solution(self, delta: float, temp: float, neighbor: Solution) -> bool:
        if neighbor.get_fitness() == float("inf"):
            return False
        if delta < 0:
            return True
        return random.random() < math.exp(
            -delta / (temp + 1e-6)
        )  # Zabezpieczenie przed dzieleniem przez 0

    def _update_history(
        self, iteration: int, temp: float, current: Solution, best: Solution
    ):
        self.history["iterations"].append(iteration)
        self.history["temperatures"].append(temp)
        self.history["current_costs"].append(current.get_fitness())
        self.history["best_costs"].append(best.get_fitness())

    def _plot_progress(self):
        plt.figure(figsize=(12, 6))
        plt.plot(
            self.history["iterations"],
            self.history["best_costs"],
            label="Najlepszy koszt",
        )
        plt.plot(
            self.history["iterations"],
            self.history["current_costs"],
            alpha=0.6,
            label="Aktualny koszt",
        )
        plt.xlabel("Iteracja")
        plt.ylabel("Fitness")
        plt.title("Postęp Symulowanego Wyżarzania")
        plt.legend()
        plt.grid(True)
        plt.show()


# Przykład użycia
if __name__ == "__main__":
    dl = DataLoader("scp41.txt")
    dl.fetch_data()
    validator = Validator(dl)

    sa = EnhancedSA(validator)
    best_solution = sa.run(debug=True)

    print(f"Best solution: {sorted(best_solution.subsets)}")
    print(f"\nNajlepsze rozwiązanie: {len(best_solution.subsets)} podzbiorów")
    print(f"Koszt: {best_solution.get_fitness():.2f}")
    print(f"Pokrycie: {'OK' if best_solution.is_correct() else 'Niekompletne'}")
