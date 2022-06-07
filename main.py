"""
Module which contains the code that runs the program

Authors: Felix Droese (felixele217)
Version: June 7th, 2022
"""

# Importing the necessary functions from algorithm.py
from algorithm import run_algorithm_for_n_points, plot_results


def main() -> None:
    """
    Runs the algorithm for n points and stores necessary valuse in a list 
    that contains the values of n from 1,...,n and its according runtimes.

    Then, it plots the results and saves them in a .png-file.
    """
    [n, times] = run_algorithm_for_n_points()
    plot_results(n, times)


if __name__ == "__main__":
    main()






