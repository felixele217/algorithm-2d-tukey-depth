"""
Module which contains the code that calculates the depth and runs the algorithm

Authors: Felix Droese (felixele217)
Version: June 7th, 2022
"""

# Importing the necessary functions and modules for the calculation
from math import sqrt, atan, pi
from random import randint
from heapq import heappop, heappush, heapify
from matplotlib import pyplot as plt
import time

def create_random_sample_points(amount_of_points: int, coordinate_range: int) -> list:
    """
    Returns a list than contains an amount of sample points in the given ranges

    Paramater amount_of_points: the amount of points which will be generated

    Parameter x_range: defines the range of the x-coordinate of the point 
    in the interval [-x_range, x_range]

    Parameter y_range: analogue to x_range
    """
    sample_points = []
    for i in range(amount_of_points):
        sample_point = create_random_sample_point(coordinate_range)
        sample_points.append(sample_point)
    return sample_points


def create_random_sample_point(coordinate_range: int) -> list:
    """
    Returns a randomly generated sample point which is
    structured like the following:
    [polar_angle, x_coordinate, y_coordinate]
    """
    x = randint(-coordinate_range, coordinate_range)
    y = randint(-coordinate_range, coordinate_range)
    while x == 0: x = randint(-coordinate_range, coordinate_range)
    while y == 0: y = randint(-coordinate_range, coordinate_range)
    polar_angle = get_polar_angle([x, y])
    return [polar_angle, x, y]


def get_polar_angle(point: list) -> float:
    """
    Returns the polar angle of a given point

    Paramter point: the point that is used for 
    calculating the polar angle
    """
    x = point[0]
    y = point[1]
    if x > 0 and y >= 0:
        polar_angle_in_radian = atan(y/x)
    elif x > 0 and y < 0:
        polar_angle_in_radian = atan(y/x) + 2*pi
    elif x < 0:
        polar_angle_in_radian = atan(y/x) + pi
    polar_angle_in_degree = 180 * polar_angle_in_radian / pi
    return polar_angle_in_degree


def divide_points_into_quadrants(sample_points: list) -> list:
    """
    Returns a list that contains the four quadrants
    quadrant_0,...,quadrant_3 with the points sorted into them

    Parameter sample_points: the list of points which will be 
    sorted into the quadrants
    """
    quadrant_0, quadrant_1, quadrant_2, quadrant_3 = ([] for i in range(4))
    for sample_point in sample_points:
        if sample_point[1] > 0 and sample_point[2] > 0: 
            quadrant_0.append(sample_point)
        elif sample_point[1] < 0 and sample_point[2] > 0:
            quadrant_1.append(sample_point)
        elif sample_point[1] < 0 and sample_point[2] < 0:
            quadrant_2.append(sample_point)
        else:
            quadrant_3.append(sample_point)
    return [quadrant_0, quadrant_1, quadrant_2, quadrant_3]


def build_heaps_for_quadrants(quadrants_with_points: list) -> list:
    """
    Returns a list that contains the heaps H_i+1 or H_i-1 for each 
    quadrant i

    Parameter quadrants_with_points: the four quadrants with the 
    sample points sorted into them
    """
    heaps_for_quadrants = []
    for index in range(len(quadrants_with_points)):
        h_i_minus_one = build_max_heap_for_quadrant_i(quadrants_with_points[(index-1) % 4])
        h_i_plus_one = build_min_heap_for_quadrant_i(quadrants_with_points[(index+1) % 4])
        heaps_for_quadrants.append([h_i_minus_one, h_i_plus_one])
    return heaps_for_quadrants


def build_max_heap_for_quadrant_i(quadrant_with_points: list) -> list:
    """
    Returns a max heap for quadrant i which is H_i-1. The property that
    is used to sort the points into heaps is the polar angle

    Parameter quadrants_with_points: the quadrant which contains the
    points that should be sorted into a max heap
    """
    h_i_minus_one = []
    heapify(h_i_minus_one)
    for point in quadrant_with_points:
        point[0] *= -1
        heappush(h_i_minus_one, point)
    for point in quadrant_with_points:
        point[0] *= -1
    return h_i_minus_one


def build_min_heap_for_quadrant_i(quadrant_with_points: list) -> list:
    """
    Returns a min heap for quadrant i which is H_i+1. The property that
    is used to sort the points into heaps is the polar angle

    Parameter quadrants_with_points: the quadrant which contains the
    points that should be sorted into a min heap
    """
    h_i_plus_one = []
    heapify(h_i_plus_one)
    for point in quadrant_with_points:
        heappush(h_i_plus_one, point)
    return h_i_plus_one


def get_extracted_elemenents_from_heaps(heaps_for_quadrants: list) -> list:
    """
    Returns the amount of extracted elements for each quadrants. The amount of extracted elements
    is calculated with iterating over the two heaps until one of the two conditions is true which
    terminates the iteration

    Parameter heaps_for_quadrants: a list with the heaps for each quadrant 
    """
    extracted_elements_counter, quadrants_with_terminated_extraction = ([] for i in range(2))

    while len(quadrants_with_terminated_extraction) != 4:
        for index in range(4):
            try:
                if (index not in quadrants_with_terminated_extraction):
                    element_from_h_i_minus_one = heappop(heaps_for_quadrants[index][0])
                    element_from_h_i_plus_one = heappop(heaps_for_quadrants[index][1])
                    extracted_elements_counter.append(index)
                    heaps_for_quadrants[index][0] = build_max_heap_for_quadrant_i(heaps_for_quadrants[index][0][1:])
                    
                    if (check_if_obtuse_angle(index, element_from_h_i_minus_one[0], element_from_h_i_plus_one[0])):
                        quadrants_with_terminated_extraction.append(index)
            except IndexError:
                quadrants_with_terminated_extraction.append(index)
    return get_extracted_elements_count(extracted_elements_counter)


def get_extracted_elements_count(extracted_elements_counter: list) -> list:
    """
    Returns the amount of extracted elements for each quadrant in a list

    Parameter extracted_elements_counter: a list that contains information
    about how many elements where extracted from the quadrants
    """
    extracted_elements_for_quadrant_i = [0, 0, 0, 0]
    for index in range(4):
        extracted_elements_for_quadrant_i[index] = extracted_elements_for_quadrant_i[index] + extracted_elements_counter.count(index)
    return extracted_elements_for_quadrant_i


def calculate_depth_i(quadrants_with_points: list, heaps_for_quadrants: list, extracted_elements_for_quadrants: list) -> list:
    """
    Returns the Tukey depth that minimizes the four quadrants which is calculated in the function scan_elements

    Parameter quadrants_with_points: the quadrants with the points

    Parameter heaps_for_quadrants: the heaps for the quadrants

    Parameter extracted_elements_for_quadrants: the amount of extracted elements for each quadrant
    """
    elements_to_scan_for_each_quadrant = [[], [], [], []]
    for index in range(len(quadrants_with_points)):
        elements_to_scan_for_each_quadrant[index] = heaps_for_quadrants[index][0][0:(2*extracted_elements_for_quadrants[index]-1)] + heaps_for_quadrants[index][1][0:(2*extracted_elements_for_quadrants[index]-1)]
        elements_to_scan_for_each_quadrant[index].sort(reverse=True)
    return scan_elements(quadrants_with_points, elements_to_scan_for_each_quadrant)


def scan_elements(quadrants_with_points: list, elements_to_scan_for_each_quadrant: list) -> int:
    """
    Returns the Tukey depth

    Parameter quadrants_with_points: the quadrants with the points

    Parameter elements_to_scan_for_each_quadrant: the elements to scan for each quadrant which are 
    already sorted depending on their polar angle, so that they can be scanned clockwise
    """
    first_point_index = [0, 0, 0, 0]
    second_point_index = [0, 0, 0, 0]
    points_in_half_space_index = [0, 0, 0, 0]
    points_in_half_space_minimum_index = [len(elements_to_scan_for_each_quadrant[0]) + len(quadrants_with_points[0]), len(elements_to_scan_for_each_quadrant[1]) + len(quadrants_with_points[1]), len(elements_to_scan_for_each_quadrant[2]) + len(quadrants_with_points[2]), len(elements_to_scan_for_each_quadrant[3]) + len(quadrants_with_points[3])] 
    quadrant_is_terminated_index = [False, False, False, False]
    while True:
        for index in range(len(elements_to_scan_for_each_quadrant)):
            if not quadrant_is_terminated_index[index]:
                if len(elements_to_scan_for_each_quadrant[index]) == 0:
                    quadrant_is_terminated_index[index] = True
                    points_in_half_space_minimum_index[index] = 0
                    continue
                if first_point_index[index] >= len(elements_to_scan_for_each_quadrant[index]) : 
                    quadrant_is_terminated_index[index] = True
                    continue
                first_point = elements_to_scan_for_each_quadrant[index][first_point_index[index] % len(elements_to_scan_for_each_quadrant[index])]
                second_point = elements_to_scan_for_each_quadrant[index][second_point_index[index] % len(elements_to_scan_for_each_quadrant[index])]
                second_point_index[index] = (second_point_index[index] + 1) % len(elements_to_scan_for_each_quadrant[index])
                points_in_half_space_index[index] = points_in_half_space_index[index] + 1
                if first_point_index[index] == second_point_index[index]:
                    first_point_index[index] = first_point_index[index] + 1
                    second_point_index[index] = second_point_index[index] + 1
                    if (points_in_half_space_index[index] < points_in_half_space_minimum_index[index]):
                        points_in_half_space_minimum_index[index] = points_in_half_space_index[index] + len(elements_to_scan_for_each_quadrant[index])
                        points_in_half_space_index[index] = 0 
                if (check_if_obtuse_angle_on_circle(first_point[0], second_point[0])):
                    first_point_index[index] = first_point_index[index] + 1 
                    if (points_in_half_space_index[index] < points_in_half_space_minimum_index[index]):
                        points_in_half_space_minimum_index[index] = points_in_half_space_index[index] + len(elements_to_scan_for_each_quadrant[index])
                        points_in_half_space_index[index] = 0  
            elif quadrant_is_terminated_index[index]:
                if (len(elements_to_scan_for_each_quadrant[index]) + points_in_half_space_index[index] <= min(points_in_half_space_minimum_index)):
                    return len(elements_to_scan_for_each_quadrant[index]) + points_in_half_space_minimum_index[index] + 1       


def check_if_obtuse_angle(index: int, polar_angle_from_h_i_minus_one: float, polar_angle_from_h_i_plus_one: float) -> bool:
    """
    Returns if the angle between two points i obtuse

    Parameter index: information about the quadrant from which the polar angle will be looked at

    Parameter polar_angle_from_h_i_minus_one: the polar angle of the point from heap H_i-1

    Parameter polar_angle_from_h_i_plus_one: the polar angle of the point from heap H_i+1
    """
    if index == 0 or index == 3:
        if (abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) < 180): 
            return True
    elif index == 1 or index == 2:
        if (360 > abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) > 180): 
            return True
    return False


def check_if_obtuse_angle_on_circle(polar_angle_from_first_pointer_point: float, polar_angle_from_second_pointer_point: float) -> bool:
    """
    Returns if the angle between to points is obtuse

    Parameter polar_angle_from_first_pointer_point: the polar angle from the first point

    Parameter polar_angle_from_second_pointer_point: the polar angle from the second point
    """
    if (abs(polar_angle_from_first_pointer_point - polar_angle_from_second_pointer_point) > 180):
        return True
    return False


def run_algorithm_for_n_points() -> list:
    """
    Returns a list that contains the values 1,...,n and the runtimes 
    for the according calculations

    First, the user is asked to enter the amount of points, 
    that should be created and the interval in which the coordinates 
    of the points are created

    Then, it begins running the algorithm for a set of 1 random point up 
    to a set of n random points and stores the runtimes in the times list
    """
    n_points = int(input("How many points do you want to create? "))
    domain = int(input("""What is the interval in which the sample points 
    should be created from [-input, input]? """))
    times = []
    for amount_of_points in range(1, n_points):
        elapsed_time = run_algorithm_for_one_set_of_points(amount_of_points, domain)
        times.append(elapsed_time)
    n=[i for i in range(1, n_points)]
    return [n, times]


def run_algorithm_for_one_set_of_points(amount_of_points: int, coordinate_range: int) -> float:
    """
    Returns the runtime needed for the calculation of the 
    tukey depth for n points

    Parameter amount_of_points: determines how many random 
    points will be generated

    Parameter coordinate_range: determines in which interval 
    the random points will be generated
    """
    sample_points = create_random_sample_points(amount_of_points, coordinate_range)
    start_time = time.time()
    quadrants_with_points = divide_points_into_quadrants(sample_points)
    heaps_for_quadrants = build_heaps_for_quadrants(quadrants_with_points)
    extracted_elements_for_quadrants = get_extracted_elemenents_from_heaps(heaps_for_quadrants)
    calculate_depth_i(quadrants_with_points, heaps_for_quadrants, extracted_elements_for_quadrants)
    return time.time() - start_time


def plot_results(n: list, times: list) -> None:
    """
    Creates the plot with the input parameters and stores it
    in an image in the plots/ subfolder

    Parameter n: amount of points

    Parameter times: times needed for the calculation
    """
    plt.xlabel("No. of elements")
    plt.ylabel("Time required")
    plt.plot(n,times)
    plt.savefig("plots/" + str(len(times) + 1) + "-points.png")
        


