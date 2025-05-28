"""This file contains visualisation classes for the Evolutionary Algorithm (EA) and Simulated Annealing (SA) implementations."""

import matplotlib.pyplot as plt
from solution import Solution
from time import sleep
from typing import List


class SA_Graph:
    """Simulated Annealing real-time-updatable graph"""

    def __init__(self, max_temp):
        plt.ion()
        self.fig, self.ax1 = plt.subplots()
        self.ax2 = self.ax1.twinx()

        self.x_data = []
        self.fitness_data = []
        self.temp_data = []

        (self.fitness_line,) = self.ax1.plot([], [], "b-", label="Fitness")
        (self.temp_line,) = self.ax2.plot([], [], "r-", label="Temperature")

        self.ax1.set_xlabel("Iteration")
        self.ax1.set_ylabel("Fitness", color="b")
        self.ax2.set_ylabel("Temperature", color="r")

        self.ax1.set_ylim(0, 0.5)  # Fitness range (0-1)
        self.ax2.set_ylim(0, max_temp)  # Temperature range (0-1000)

        self.ax1.grid(True, alpha=0.3)
        self.ax2.grid(True, alpha=0.3)
        self.fig.tight_layout()

        lines = [self.fitness_line, self.temp_line]
        self.ax1.legend(lines, [l.get_label() for l in lines], loc="upper left")

    def update_graph(self, fitness: float, temp: float) -> None:
        """Add another point to graph

        Args:
            fitness (float): Solution.get_fitness()
            temp (float): Iterator from SA loop
        """
        self.x_data.append(len(self.x_data))
        self.fitness_data.append(fitness)
        self.temp_data.append(temp)

        self.fitness_line.set_data(self.x_data, self.fitness_data)
        self.temp_line.set_data(self.x_data, self.temp_data)

        self.ax1.relim()
        self.ax1.autoscale_view(scalex=True, scaley=False)
        self.ax2.relim()
        self.ax2.autoscale_view(scalex=False, scaley=False)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


class EA_Graph:
    """Evolutionary Algorithm real-time-updatable graph"""

    def __init__(self, generations: int = 200) -> None:
        self.generations = generations
        plt.ion()
        self.fig, self.ax = plt.subplots()

        self.x_data = []
        self.best_data = []
        self.avg_data = []
        self.worst_data = []

        (self.best_line,) = self.ax.plot([], [], "g-", label="Best Fitness")
        (self.avg_line,) = self.ax.plot([], [], "b-", label="Average Fitness")
        (self.worst_line,) = self.ax.plot([], [], "r-", label="Worst Fitness")

        self.ax.set_xlabel("Generation")
        self.ax.set_ylabel("Fitness")
        self.ax.set_title("Evolutionary Algorithm Progress")
        self.ax.legend(loc="upper right")
        self.ax.grid(True)

        self.ax.set_xlim(0, generations)
        self.ax.set_ylim(0, 0.6)

    def update_graph(self, solutions: List[Solution]) -> None:
        """Add another generation to graph

        Args:
            solutions (List[Solution]): Single generation
        """

        fitness_values = [s.get_fitness() for s in solutions]

        current_best = min(fitness_values)
        current_worst = max(fitness_values)
        current_avg = sum(fitness_values) / len(fitness_values)

        generation_num = len(self.x_data)
        self.x_data.append(generation_num)
        self.best_data.append(current_best)
        self.avg_data.append(current_avg)
        self.worst_data.append(current_worst)

        self.best_line.set_data(self.x_data, self.best_data)
        self.avg_line.set_data(self.x_data, self.avg_data)
        self.worst_line.set_data(self.x_data, self.worst_data)

        self.ax.relim()
        self.ax.autoscale_view(scalex=True, scaley=True)

        self.fig.canvas.draw()
        self.fig.canvas.flush_events()


def plot_histories(best_hist, avg_hist, worst_hist):
    """
    Plots three performance histories (best, average, worst) using matplotlib.

    Parameters:
    best_hist (list): List of best performance values (floats)
    avg_hist (list): List of average performance values (floats)
    worst_hist (list): List of worst performance values (floats)
    """
    # Create x-axis values (0 to n-1)
    x = list(range(len(best_hist)))

    # Create figure and axis
    plt.figure(figsize=(10, 6))

    # Plot all three histories
    plt.plot(x, best_hist, "b-", label="Best", linewidth=2)
    plt.plot(x, avg_hist, "g-", label="Average", linewidth=2)
    plt.plot(x, worst_hist, "r-", label="Worst", linewidth=2)

    # Add labels and title
    plt.xlabel("Generation")
    plt.ylabel("Fitness Value")
    plt.title("Fitnes over generations graph")
    plt.grid(True, linestyle="--", alpha=0.7)
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()
