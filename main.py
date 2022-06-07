from math import sqrt
from algorithm import *
import time
import matplotlib.pyplot as plt


def main(): 
    [n, times] = run_algorithm_for_n_points(n_points=5000)
    plot_results(n, times)


if __name__ == "__main__":
    main()