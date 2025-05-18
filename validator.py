from solution import Solution


class Validator:
    def __init__(self, n, m, costs, covers):
        """Subclass for simulation used for calculating various things

        Args:
            n (int): Number of elements that need to be covered
            m (int): Number of subsets that can be choosen
            costs (List[int]): Costs of subsets
            covers (List[List[int]]): Elements covered by each subset
        """
        self.n = n
        self.m = m
        self.costs = costs
        self.covers = covers
        pass

    def is_correct(solution: Solution) -> bool:
        """Check if solution covers all elements

        Args:
            solution (Solution): Solution object to check

        Returns:
            bool: True if all elements are covered
        """
        # TODO Implement
        return True

    def sum_costs(solution: Solution) -> int:
        """Calculate sum of subsets' costs from a solution

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            int: Sum of costs
        """
        # TODO Implement
        return 10

    def calculate_fitness(solution: Solution) -> float:
        """Calculate solutions fitness based on covered elements and cost

        Args:
            solution (Solution): Solution to calculate for

        Returns:
            float: Fitness indicator
        """
        # TODO Implement
        return 0.5
