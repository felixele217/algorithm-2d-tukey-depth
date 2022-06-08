"""
Module which contains the code that runs the program

Authors: Felix Droese (felixele217)
Version: June 7th, 2022
"""

# Importing the necessary functions from algorithm.py
from algorithm import run_algorithm_for_n_points, plot_results


def main() -> None:
    """
    Runs the algorithm for n points and stores necessary values in a list 
    that contains the values of n from 1,...,n and its according runtimes.

    Then, it plots the results and saves them in a .png-file.
    """
    [n, times] = run_algorithm_for_n_points()
    plot_results(n, times)


if __name__ == "__main__":
    """
    Runs the main function, if the condition is true.

    The condition is true, if the code is run directly from this file like it 
    is in 'python3 main.py'.
    """
    main()






