from math import sqrt
from algorithm import *
import time
import matplotlib.pyplot as plt


def run_algorithm_for_n_points(n_points):
    times = []
    for amount_of_points in range(1, n_points):
        elapsed_time = run_algorithm_for_one_point(amount_of_points)
        times.append(elapsed_time)
    n=[i for i in range(1, n_points)]
    return [n, times]


def run_algorithm_for_one_point(amount_of_points):
    sample_points = create_random_sample_points(amount_of_points, 100, 100)
    start_time = time.time()
    quadrants_with_points = divide_points_into_quadrants(sample_points)
    heaps_for_quadrants = build_heaps_for_quadrants(quadrants_with_points)
    extracted_elements_for_quadrants = get_extracted_elemenents_from_heaps(quadrants_with_points, heaps_for_quadrants)
    calculate_depth_i(quadrants_with_points, heaps_for_quadrants, extracted_elements_for_quadrants)
    return time.time() - start_time


def plot_results(n, times):
    # matplotlib.interactive(True)
    plt.xlabel("No. of elements")
    plt.ylabel("Time required")
    plt.plot(n,times)
    # plt.show()
    plt.savefig("plots/" + str(len(times) + 1) + "-points.png")


def main(): 
    [n, times] = run_algorithm_for_n_points(n_points=10000)
    plot_results(n, times)


if __name__ == "__main__":
    main()