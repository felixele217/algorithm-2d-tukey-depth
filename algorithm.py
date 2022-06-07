from math import sqrt, atan, pi
from random import randint
from heapq import heappop, heappush, heapify
from matplotlib import pyplot as plt
import time

# Erstellen von zufälligen Punkten, die für die Berechnung der Tukey depth dienen
def create_random_sample_points(amount_of_points, x_range, y_range):
    sample_points = []
    for i in range(amount_of_points):
        sample_point = create_random_sample_point(x_range, y_range)
        sample_points.append(sample_point)
    return sample_points


# Funktion zum Erstellen von einem zufälligen Punkt
def create_random_sample_point(x_range, y_range):
    x = randint(-x_range, x_range)
    y = randint(-y_range, y_range)
    while x == 0: x = randint(-x_range, x_range)
    while y == 0: y = randint(-y_range, y_range)
    polar_angle = get_polar_angle([x, y])
    return [polar_angle, x, y]


# Berechnen des Polarwinkels für einen Punkt 
def get_polar_angle(point):
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


# Aufteilen der Punkte aus der Punktmenge in unterschiedliche Quadranten
def divide_points_into_quadrants(sample_points):
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


# Bilden der Heaps für einen Quadranten i
def build_heaps_for_quadrants(quadrants_with_points):
    heaps_for_quadrants = []
    for index in range(len(quadrants_with_points)):
        h_i_minus_one = build_max_heap_for_quadrant_i(quadrants_with_points[(index-1) % 4])
        h_i_plus_one = build_min_heap_for_quadrant_i(quadrants_with_points[(index+1) % 4])
        heaps_for_quadrants.append([h_i_minus_one, h_i_plus_one])
    # print("MAX HEAP:", h_i_minus_one)
    # print("MIN HEAP:", h_i_plus_one)
    return heaps_for_quadrants


# Bilden eines max heaps für einen Quadranten i
def build_max_heap_for_quadrant_i(quadrant_with_points):
    h_i_minus_one = []
    heapify(h_i_minus_one)
    for point in quadrant_with_points:
        point[0] *= -1
        heappush(h_i_minus_one, point)
    for point in quadrant_with_points:
        point[0] *= -1
    return h_i_minus_one


# Bilden eines min heaps für einen Quadranten i
def build_min_heap_for_quadrant_i(quadrant_with_points):
    h_i_plus_one = []
    heapify(h_i_plus_one)
    for point in quadrant_with_points:
        heappush(h_i_plus_one, point)
    return h_i_plus_one


def get_extracted_elemenents_from_heaps(quadrants_with_points, heaps_for_quadrants):
    extracted_elements_counter, quadrants_with_terminated_extraction = ([] for i in range(2))

    while len(quadrants_with_terminated_extraction) != 4:
        for index in range(len(quadrants_with_points)):
            try:
                if (index not in quadrants_with_terminated_extraction):
                    element_from_h_i_minus_one = heappop(heaps_for_quadrants[index][0]) # heaps_for_quadrants[index][0][0]
                    element_from_h_i_plus_one = heappop(heaps_for_quadrants[index][1])
                    extracted_elements_counter.append(index)
                    heaps_for_quadrants[index][0] = build_max_heap_for_quadrant_i(heaps_for_quadrants[index][0][1:])
                    
                    if (check_if_obtuse_angle(index, element_from_h_i_minus_one[0], element_from_h_i_plus_one[0])):
                        quadrants_with_terminated_extraction.append(index)
            except IndexError:
                quadrants_with_terminated_extraction.append(index)
    
    return get_extracted_elements_count(extracted_elements_counter)


def calculate_depth_i(quadrants_with_points, heaps_for_quadrants, extracted_elements_for_quadrants):
    elements_to_scan_for_each_quadrant = [[], [], [], []]
    for index in range(len(quadrants_with_points)):
        # hier weiß ich noch nicht so richtig, ob das stimmt, da die modified heaps einfach immer genau wie die unmodified heaps sind. bruder egal
        elements_to_scan_for_each_quadrant[index] = heaps_for_quadrants[index][0][0:(2*extracted_elements_for_quadrants[index]-1)] + heaps_for_quadrants[index][1][0:(2*extracted_elements_for_quadrants[index]-1)]
        elements_to_scan_for_each_quadrant[index].sort(reverse=True)
    return scan_elements(quadrants_with_points, elements_to_scan_for_each_quadrant)


def scan_elements(quadrants_with_points, elements_to_scan_for_each_quadrant):
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


def check_if_obtuse_angle(index, polar_angle_from_h_i_minus_one, polar_angle_from_h_i_plus_one):
    if index == 0 or index == 3:
        if (abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) < 180): 
            return True
    elif index == 1 or index == 2:
        if (360 > abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) > 180): 
            return True
    return False


def check_if_obtuse_angle_on_circle(polar_angle_from_first_pointer_point, polar_angle_from_second_pointer_point):
    if (abs(polar_angle_from_first_pointer_point - polar_angle_from_second_pointer_point) > 180):
        return True
    return False


def get_extracted_elements_count(extracted_elements_counter):
    extracted_elements_for_quadrant_i = [0, 0, 0, 0]
    for index in range(4):
        extracted_elements_for_quadrant_i[index] = extracted_elements_for_quadrant_i[index] + extracted_elements_counter.count(index)
    return extracted_elements_for_quadrant_i


def run_algorithm_for_n_points(n_points):
    times = []
    for amount_of_points in range(1, n_points):
        elapsed_time = run_algorithm_for_one_point(amount_of_points)
        times.append(elapsed_time)
    n=[i for i in range(1, n_points)]
    return [n, times]


def run_algorithm_for_one_point(amount_of_points):
    sample_points = create_random_sample_points(amount_of_points, x_range=100, y_range=100)
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
        


