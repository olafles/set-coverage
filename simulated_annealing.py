"""This file contains the Simulated Annealing algorithm implementation for the Set Cover Problem (SCP)."""

from validator import Validator
from DataLoader import DataLoader
from solution import Solution
from mutations import Mutations
from random_correct import RandomSolutionGenerator
import random
import math
from typing import Literal
import matplotlib.pyplot as plt


class SimulatedAnnealing:
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
        cooling_rate: float = 0.99,
        cooling_strategy: Literal[
            "exponential", "linear", "logarithmic"
        ] = "exponential",
        max_iterations: int = 100000,
        debug: bool = False,
        draw: bool = False,
    ) -> Solution:
        """Run the Simulated Annealing algorithm to find the best solution.

        Args:
            initial_temp (float): Initial temperature for the algorithm.
            min_temp (float): Minimum temperature to stop the algorithm.
            cooling_rate (float): Rate at which the temperature decreases (for exponential)
                                 or step size (for linear/logarithmic).
            cooling_strategy (str): Cooling strategy - "exponential", "linear", or "logarithmic".
            max_iterations (int): Maximum number of iterations to run.
            debug (bool): If True, print debug information during execution.
            draw (bool): If True, plot the progress after completion.

        Returns:
            Solution: The best solution found by the algorithm.
        """
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
                    f"Iter: {iteration}, Temp: {temperature:.6f}, Current fitness: {current.get_fitness():.6f}, Best fitness: {best.get_fitness():.6f}"
                )

            temperature = self._update_temperature(
                temperature, initial_temp, iteration, cooling_rate, cooling_strategy
            )
            iteration += 1

            self._update_history(iteration, temperature, current, best)

        if draw:
            self._plot_progress()

        return best

    def _update_temperature(
        self,
        current_temp: float,
        initial_temp: float,
        iteration: int,
        cooling_rate: float,
        strategy: str,
    ) -> float:
        """Update temperature based on the selected cooling strategy.

        Args:
            current_temp (float): Current temperature.
            initial_temp (float): Initial temperature.
            iteration (int): Current iteration number.
            cooling_rate (float): Cooling parameter.
            strategy (str): Cooling strategy to use.

        Returns:
            float: Updated temperature.
        """
        if strategy == "exponential":
            return current_temp * cooling_rate
        elif strategy == "linear":
            return max(initial_temp - iteration * cooling_rate)
        elif strategy == "logarithmic":
            return initial_temp / (1 + cooling_rate * math.log(1 + iteration))
        else:
            raise ValueError(f"Unknown cooling strategy: {strategy}")

    def _generate_neighbor(self, solution: Solution) -> Solution:
        """Generate a neighbor solution by applying a mutation.

        Args:
            solution (Solution): The current solution to mutate.

        Returns:
            Solution: A neighbor solution generated by mutation.
        """
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
        """Determine whether to accept the neighbor solution based on the acceptance criteria.

        Args:
            delta (float): Change in fitness between the neighbor and current solution.
            temp (float): Current temperature of the system.
            neighbor (Solution): The neighbor solution to evaluate.

        Returns:
            bool: True if the neighbor solution should be accepted, False otherwise.
        """
        if neighbor.get_fitness() == float("inf"):
            return False
        if delta < 0:
            return True
        return random.random() < math.exp(-delta / (temp + 1e-6))

    def _update_history(
        self, iteration: int, temp: float, current: Solution, best: Solution
    ):
        """Update the history of the algorithm's progress.

        Args:
            iteration (int): Current iteration number.
            temp (float): Current temperature of the system.
            current (Solution): The current solution.
            best (Solution): The best solution found so far.
        """
        self.history["iterations"].append(iteration)
        self.history["temperatures"].append(temp)
        self.history["current_costs"].append(current.get_fitness())
        self.history["best_costs"].append(best.get_fitness())

    def _plot_progress(self):
        """Plot the progress of the algorithm showing cost evolution and temperature on one chart."""
        fig, ax1 = plt.subplots(1, 1, figsize=(12, 8))

        line1 = ax1.plot(
            self.history["iterations"],
            self.history["best_costs"],
            label="Najlepszy koszt",
            color="blue",
            linewidth=2,
        )
        line2 = ax1.plot(
            self.history["iterations"],
            self.history["current_costs"],
            alpha=0.6,
            label="Aktualny koszt",
            color="orange",
            linewidth=1.5,
        )

        ax1.set_xlabel("Iteracja")
        ax1.set_ylabel("Fitness", color="blue")
        ax1.tick_params(axis="y", labelcolor="blue")
        ax1.grid(True, alpha=0.3)

        ax2 = ax1.twinx()
        line3 = ax2.plot(
            self.history["iterations"],
            self.history["temperatures"],
            label="Temperatura",
            color="red",
            linewidth=2,
            linestyle="--",
        )
        ax2.set_ylabel("Temperatura", color="red")
        ax2.tick_params(axis="y", labelcolor="red")
        ax2.set_yscale("log")

        lines = line1 + line2 + line3
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc="upper right")

        plt.title("Postęp Symulowanego Wyżarzania - Koszt i Temperatura")
        plt.tight_layout()
        plt.show()


# Przykład użycia
if __name__ == "__main__":
    dl = DataLoader("scp41.txt")
    dl.fetch_data()
    vd = Validator(dl)

    sa = SimulatedAnnealing(vd)
    test_sa = sa.run(
        initial_temp=2000.0,
        min_temp=0.000001,
        cooling_rate=0.9995,
        max_iterations=100000,
        cooling_strategy="exponential",
        debug=True,
        draw=True,
    )

    print(f"Best solution: {sorted(test_sa.subsets)}")
    print(f"\nNajlepsze rozwiązanie: {len(test_sa.subsets)} podzbiorów")
    print(f"Najlepszy fitness: {test_sa.get_fitness():.6f}")
    print(f"Pokrycie: {'OK' if test_sa.is_correct() else 'Niekompletne'}")
