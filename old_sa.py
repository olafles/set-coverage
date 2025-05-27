from validator import Validator
from random_correct import RandomSolutionGenerator
from solution import Solution
from mutations import Mutations
from math import exp, log
import random
from visualiser import SA_Graph
from greedy import GreedySolutionGenerator


class SimulatedAnnealing:
    def __init__(self, validator: Validator) -> None:
        self.validator = validator
        self.rsa = RandomSolutionGenerator(self.validator)
        self.gsg = GreedySolutionGenerator(self.validator)

    def run(
        self,
        initial_temp: float = 100.0,
        final_temp: float = 0.1,
        max_iterations: int = 10000,
        start_greedy: bool = True,
        draw: bool = False,
        cooling_schedule: str = "linear",  # "linear", "exponential", "logarithmic"
    ) -> Solution:
        """
        Run Simulated Annealing (SA) algorithm.

        Args:
            initial_temp: Starting temperature
            final_temp: Final temperature
            max_iterations: Maximum number of iterations
            start_greedy: Whether to start with greedy solution
            draw: Whether to visualize progress
            cooling_schedule: Type of cooling schedule to use
        """
        if draw:
            self.graph = SA_Graph(max_temp=initial_temp)

        if start_greedy:
            current_solution = self.gsg._generate_greedy_solution()
        else:
            current_solution = self.rsa.generate_random_solution()

        self.validator.complex_eval(current_solution)
        best_solution = current_solution

        temperature = initial_temp
        iteration = 0

        while iteration < max_iterations and temperature < final_temp:
            mutation_choice = random.choice(["swap", "add", "remove", "local_search"])

            if mutation_choice == "swap":
                neighbor = Mutations.swap_mutation(current_solution, self.validator)
            elif mutation_choice == "add":
                neighbor = Mutations.add_mutation(current_solution, self.validator)
            elif mutation_choice == "remove":
                neighbor = Mutations.remove_mutation(current_solution, self.validator)
            else:  # ls
                neighbor = Solution(list(current_solution.subsets))
                self.validator.remove_redundant_subsets(neighbor, continuous=True)
                self.validator.complex_eval(neighbor)

            fitness_diff = neighbor.get_fitness() - current_solution.get_fitness()

            if fitness_diff < 0:
                current_solution = neighbor
            elif temperature > 0:
                acceptance_prob = exp(-fitness_diff / temperature)
                if random.random() < acceptance_prob:
                    current_solution = neighbor

            if current_solution.get_fitness() < best_solution.get_fitness():
                best_solution = Solution(list(current_solution.subsets))
                self.validator.complex_eval(best_solution)

            if draw:
                self.graph.update_graph(current_solution.get_fitness(), temperature)

            temperature = self._cool_temperature(
                initial_temp, final_temp, iteration, max_iterations, cooling_schedule
            )
            iteration += 1

        if draw:
            input("Press enter to close and continue")

        return best_solution

    def _cool_temperature(
        self, initial_temp, final_temp, iteration, max_iterations, schedule
    ):
        """Different cooling schedules for temperature reduction."""
        progress = iteration / max_iterations

        if schedule == "linear":
            return initial_temp * (1 - progress) + final_temp * progress
        elif schedule == "exponential":
            alpha = (final_temp / initial_temp) ** (1 / max_iterations)
            return initial_temp * (alpha**iteration)
        elif schedule == "logarithmic":
            if iteration == 0:
                return initial_temp
            return initial_temp / log(iteration + 2)
        else:
            return initial_temp * (1 - progress)
