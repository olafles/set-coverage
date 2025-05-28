"""This file contains Evolutionary Algorithm (EA) implementation for the Set Cover Problem (SCP)."""

from typing import List, Tuple
import random
from solution import Solution
from validator import Validator
from population import PopulationGenerator
from selections import Selection
from crossovers import Crossovers
from mutations import Mutations
from visualiser import plot_histories


class EvolutionaryAlgorithm:
    def __init__(
        self,
        validator: Validator,
        population_size: int = 50,
        mutation_rate: float = 0.1,
        crossover_rate: float = 0.8,
        tournament_size: int = 3,
        elitism_count: int = 2,
        crossover_method: str = "uniform",  # uniform, greedy, pmx
        mutation_method: str = "swap",  # add, remove, swap
        selection_method: str = "tournament",  # tournament, roulette
    ):
        """
        Initialize the Evolutionary Algorithm.

        Args:
            validator: Validator instance for the Set Cover Problem
            population_size: Size of the population
            mutation_rate: Probability of mutation (0.0 to 1.0)
            crossover_rate: Probability of crossover (0.0 to 1.0)
            tournament_size: Size of tournament for tournament selection
            elitism_count: Number of best solutions to carry over unchanged
            crossover_method: Crossover method ("uniform", "greedy", "pmx")
            mutation_method: Mutation method ("add", "remove", "swap")
            selection_method: Selection method ("tournament", "roulette")
        """
        self.validator = validator
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.tournament_size = tournament_size
        self.elitism_count = elitism_count

        self.crossover_method = crossover_method.lower()
        self.mutation_method = mutation_method.lower()
        self.selection_method = selection_method.lower()

        self._validate_methods()

        self.best_fitness_history = []
        self.avg_fitness_history = []
        self.best_solution = None

    def _validate_methods(self) -> None:
        """Validate that the chosen methods are available."""
        valid_crossovers = ["uniform", "greedy", "pmx"]
        valid_mutations = ["add", "remove", "swap"]
        valid_selections = ["tournament", "roulette"]

        if self.crossover_method not in valid_crossovers:
            raise ValueError(
                f"Invalid crossover method: {self.crossover_method}. "
                f"Valid options: {valid_crossovers}"
            )

        if self.mutation_method not in valid_mutations:
            raise ValueError(
                f"Invalid mutation method: {self.mutation_method}. "
                f"Valid options: {valid_mutations}"
            )

        if self.selection_method not in valid_selections:
            raise ValueError(
                f"Invalid selection method: {self.selection_method}. "
                f"Valid options: {valid_selections}"
            )

        print(f"EA Configuration:")
        print(f"  Crossover: {self.crossover_method}")
        print(f"  Mutation: {self.mutation_method}")
        print(f"  Selection: {self.selection_method}")

    def run(
        self, generations: int, verbose: bool = True, draw: bool = False
    ) -> Tuple[Solution, List[float], List[float]]:
        """
        Run the evolutionary algorithm for specified number of generations.

        Args:
            generations: Number of generations to run
            verbose: Whether to print progress information

        Returns:
            Tuple of (best_solution, best_fitness_history, avg_fitness_history)
        """
        if draw:
            best_history = []
            avg_history = []
            worst_history = []
        if verbose:
            print("Initializing population...")
        population = PopulationGenerator.generate_initial_population(
            self.population_size, self.validator
        )

        for generation in range(generations):
            self._evaluate_population(population)

            current_best = min(population, key=lambda sol: sol.get_fitness())
            current_worst = max(population, key=lambda sol: sol.get_fitness())
            avg_fitness = sum(sol.get_fitness() for sol in population) / len(population)
            if draw:
                best_history.append(current_best.get_fitness())
                worst_history.append(current_worst.get_fitness())
                avg_history.append(avg_fitness)
            if (
                self.best_solution is None
                or current_best.get_fitness() < self.best_solution.get_fitness()
            ):
                self.best_solution = Solution(list(current_best.subsets))
                self.validator.complex_eval(self.best_solution)

            if verbose and (generation % 10 == 0 or generation == generations - 1):
                print(
                    f"Generation {generation}: Best fitness = {current_best.get_fitness():.4f}, "
                    f"Avg fitness = {avg_fitness:.4f}, Best cost = {current_best.get_cost_sum()}"
                )

            new_population = self._create_new_population(population)
            population = new_population

        if draw:
            plot_histories(best_history, avg_history, worst_history)
            input("Press Enter to close the graph window...")
        return self.best_solution, self.best_fitness_history, self.avg_fitness_history

    def _evaluate_population(self, population: List[Solution]) -> None:
        """Evaluate all solutions in the population and update statistics.

        Args:
            population: List of solutions to evaluate
        """
        fitness_values = []

        for solution in population:
            self.validator.complex_eval(solution)
            fitness_values.append(solution.get_fitness())

        self.best_fitness_history.append(min(fitness_values))
        self.avg_fitness_history.append(sum(fitness_values) / len(fitness_values))

    def _create_new_population(self, population: List[Solution]) -> List[Solution]:
        """Create a new population using selection, crossover, and mutation.

        Args:
            population: List of current solutions

        Returns:
            List[Solution]: New population of solutions
        """
        new_population = []

        if self.elitism_count > 0:
            elite = sorted(population, key=lambda sol: sol.get_fitness())[
                : self.elitism_count
            ]
            new_population.extend([Solution(list(sol.subsets)) for sol in elite])

        while len(new_population) < self.population_size:
            parents = self._perform_selection(population, num_parents=2)
            parent1, parent2 = parents[0], parents[1]

            if random.random() < self.crossover_rate:
                child = self._perform_crossover(parent1, parent2)
            else:
                child = Solution(list(random.choice([parent1, parent2]).subsets))

            if random.random() < self.mutation_rate:
                child = self._perform_mutation(child)

            self.validator.complex_eval(child)
            new_population.append(child)

        return new_population[: self.population_size]

    def _perform_selection(
        self, population: List[Solution], num_parents: int
    ) -> List[Solution]:
        """Perform selection based on the chosen method.

        Args:
            population: List of current solutions
            num_parents: Number of parents to select

        Returns:
            List[Solution]: Selected parents
        """
        if self.selection_method == "tournament":
            return Selection.tournament_selection(
                population, num_parents, self.tournament_size
            )
        elif self.selection_method == "roulette":
            return Selection.roulette_selection(population, num_parents)
        else:
            raise ValueError(f"Unknown selection method: {self.selection_method}")

    def _perform_crossover(self, parent1: Solution, parent2: Solution) -> Solution:
        """Perform crossover based on the chosen method.

        Args:
            parent1: First parent solution
            parent2: Second parent solution

        Returns:
            Solution: Child solution created from parents
        """
        if self.crossover_method == "uniform":
            return Crossovers.uniform_crossover(parent1, parent2, self.validator)
        elif self.crossover_method == "greedy":
            return Crossovers.greedy_crossover(parent1, parent2, self.validator)
        elif self.crossover_method == "pmx":
            return Crossovers.pmx_crossover(parent1, parent2, self.validator)
        else:
            raise ValueError(f"Unknown crossover method: {self.crossover_method}")

    def _perform_mutation(self, solution: Solution) -> Solution:
        """Perform mutation based on the chosen method.

        Args:
            solution: Solution to mutate

        Returns:
            Solution: Mutated solution
        """
        if self.mutation_method == "add":
            return Mutations.add_mutation(solution, self.validator)
        elif self.mutation_method == "remove":
            return Mutations.remove_mutation(solution, self.validator)
        elif self.mutation_method == "swap":
            return Mutations.swap_mutation(solution, self.validator)
        else:
            raise ValueError(f"Unknown mutation method: {self.mutation_method}")

    def get_statistics(self) -> dict:
        """Get algorithm statistics.

        Returns:
            dict: Dictionary with statistics
        """
        if not self.best_solution:
            return {}

        return {
            "best_fitness": self.best_solution.get_fitness(),
            "best_cost": self.best_solution.get_cost_sum(),
            "best_subsets": sorted(self.best_solution.subsets),
            "num_subsets": len(self.best_solution.subsets),
            "generations_run": len(self.best_fitness_history),
            "crossover_method": self.crossover_method,
            "mutation_method": self.mutation_method,
            "selection_method": self.selection_method,
        }

    def set_parameters(
        self,
        population_size: int = None,
        mutation_rate: float = None,
        crossover_rate: float = None,
        tournament_size: int = None,
        elitism_count: int = None,
        crossover_method: str = None,
        mutation_method: str = None,
        selection_method: str = None,
    ) -> None:
        """Update algorithm parameters.

        Args:
            population_size: New population size
            mutation_rate: New mutation rate
            crossover_rate: New crossover rate
            tournament_size: New tournament size
            elitism_count: New elitism count
            crossover_method: New crossover method
            mutation_method: New mutation method
            selection_method: New selection method
        """
        if population_size is not None:
            self.population_size = population_size
        if mutation_rate is not None:
            self.mutation_rate = mutation_rate
        if crossover_rate is not None:
            self.crossover_rate = crossover_rate
        if tournament_size is not None:
            self.tournament_size = tournament_size
        if elitism_count is not None:
            self.elitism_count = elitism_count
        if crossover_method is not None:
            self.crossover_method = crossover_method.lower()
        if mutation_method is not None:
            self.mutation_method = mutation_method.lower()
        if selection_method is not None:
            self.selection_method = selection_method.lower()

        if any([crossover_method, mutation_method, selection_method]):
            self._validate_methods()


class EvolutionaryAlgorithmComparison:
    """Utility class for comparing different EA configurations."""

    @staticmethod
    def compare_configurations(
        validator: Validator,
        configurations: List[dict],
        generations: int = 100,
        runs_per_config: int = 5,
    ) -> dict:
        """
        Compare different EA configurations.

        Args:
            validator: Validator instance
            configurations: List of configuration dictionaries
            generations: Number of generations per run
            runs_per_config: Number of runs per configuration

        Returns:
            Dictionary with comparison results
        """
        results = {}

        for i, config in enumerate(configurations):
            print(f"Testing configuration {i+1}/{len(configurations)}: {config}")

            run_results = []
            for run in range(runs_per_config):
                ea = EvolutionaryAlgorithm(validator, **config)
                best_solution, _, _ = ea.run(generations, verbose=False)
                run_results.append(
                    {
                        "fitness": best_solution.get_fitness(),
                        "cost": best_solution.get_cost_sum(),
                        "subsets_count": len(best_solution.subsets),
                    }
                )

            fitnesses = [r["fitness"] for r in run_results]
            costs = [r["cost"] for r in run_results]

            results[f"config_{i+1}"] = {
                "configuration": config,
                "avg_fitness": sum(fitnesses) / len(fitnesses),
                "best_fitness": min(fitnesses),
                "worst_fitness": max(fitnesses),
                "avg_cost": sum(costs) / len(costs),
                "best_cost": min(costs),
                "worst_cost": max(costs),
                "runs": run_results,
            }

        return results

    @staticmethod
    def compare_methods(
        validator: Validator, generations: int = 100, runs_per_method: int = 3
    ) -> dict:
        """
        Compare different combinations of crossover, mutation, and selection methods.

        Args:
            validator: Validator instance
            generations: Number of generations per run
            runs_per_method: Number of runs per method combination

        Returns:
            Dictionary with method comparison results
        """
        crossover_methods = ["uniform", "greedy", "pmx"]
        mutation_methods = ["add", "remove", "swap"]
        selection_methods = ["tournament", "roulette"]

        results = {}
        total_combinations = (
            len(crossover_methods) * len(mutation_methods) * len(selection_methods)
        )
        current_combination = 0

        for crossover in crossover_methods:
            for mutation in mutation_methods:
                for selection in selection_methods:
                    current_combination += 1
                    method_name = f"{crossover}_{mutation}_{selection}"

                    print(
                        f"Testing combination {current_combination}/{total_combinations}: "
                        f"Crossover={crossover}, Mutation={mutation}, Selection={selection}"
                    )

                    run_results = []
                    for run in range(runs_per_method):
                        ea = EvolutionaryAlgorithm(
                            validator,
                            crossover_method=crossover,
                            mutation_method=mutation,
                            selection_method=selection,
                        )
                        best_solution, _, _ = ea.run(generations, verbose=False)
                        run_results.append(
                            {
                                "fitness": best_solution.get_fitness(),
                                "cost": best_solution.get_cost_sum(),
                                "subsets_count": len(best_solution.subsets),
                            }
                        )

                    fitnesses = [r["fitness"] for r in run_results]
                    costs = [r["cost"] for r in run_results]

                    results[method_name] = {
                        "crossover": crossover,
                        "mutation": mutation,
                        "selection": selection,
                        "avg_fitness": sum(fitnesses) / len(fitnesses),
                        "best_fitness": min(fitnesses),
                        "worst_fitness": max(fitnesses),
                        "avg_cost": sum(costs) / len(costs),
                        "best_cost": min(costs),
                        "worst_cost": max(costs),
                        "runs": run_results,
                    }

        return results
