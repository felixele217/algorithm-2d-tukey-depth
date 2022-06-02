from math import sqrt, atan, pi, inf
from random import randint
from heapq import heappop, heappush, heapify

# Erstellen von zufälligen Punkten, die für die Berechnung der Tukey depth dienen
def create_random_sample_points():
    amount_of_points = int(input("How many points do you want to create? "))
    sample_points = []
    for i in range(amount_of_points):
        sample_point = create_random_sample_point()
        sample_points.append(sample_point)
    return sample_points


# Funktion zum Erstellen von einem zufälligen Punkt
def create_random_sample_point():
    x = randint(-100, 100)
    y = randint(-100, 100)
    while x == 0: x = randint(-100, 100)
    while y == 0: y = randint(-100, 100)
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
    return scan_elements(elements_to_scan_for_each_quadrant)


def scan_elements(elements_to_scan_for_each_quadrant):
    points_in_half_space_counter_for_iteration = [0, 0, 0, 0]
    points_in_half_space_minimum = [inf, inf, inf, inf]
    first_pointer_index = [0, 0, 0, 0]
    second_pointer_index = [0, 0, 0, 0]
    quadrant_is_terminated = [False, False, False, False]
    index_error = False
    points_to_scan = [len(elements_to_scan_for_each_quadrant[0]), len(elements_to_scan_for_each_quadrant[1]), len(elements_to_scan_for_each_quadrant[2]), len(elements_to_scan_for_each_quadrant[3])]
    while True:
        for index in range(len(elements_to_scan_for_each_quadrant)):
            if (first_pointer_index[index] > points_to_scan[index]):
                quadrant_is_terminated[index] = True
            if not quadrant_is_terminated[index]:
                first_pointer_for_quadrant_i = elements_to_scan_for_each_quadrant[index][first_pointer_index[index] % points_to_scan[index]]
                second_pointer_for_quadrant_i = elements_to_scan_for_each_quadrant[index][second_pointer_index[index] % points_to_scan[index]]
                second_pointer_index[index] = (second_pointer_index[index] + 1) % points_to_scan[index]
                points_in_half_space_counter_for_iteration[index] = points_in_half_space_counter_for_iteration[index] + 1 
                if (first_pointer_index[index] is second_pointer_index[index]):
                    if (points_in_half_space_counter_for_iteration[index] < points_in_half_space_minimum[index]):
                        points_in_half_space_minimum[index] = points_in_half_space_counter_for_iteration[index]
                        points_in_half_space_counter_for_iteration[index] = 0
                # try:
                #     second_pointer_index[index] = second_pointer_index[index] + 1
                # except IndexError:
                #     first_pointer_index[index] = first_pointer_index[index] + 1 
                #     index_error = True
                #     if (points_in_half_space_counter_for_iteration[index] < points_in_half_space_minimum[index]):
                #         points_in_half_space_minimum[index] = points_in_half_space_counter_for_iteration[index]
                #         points_in_half_space_counter_for_iteration[index] = 0
                if (check_if_obtuse_angle(index, first_pointer_for_quadrant_i[0], second_pointer_for_quadrant_i[0]) and not index_error):
                    first_pointer_index[index] = first_pointer_index[index] + 1
                    if (points_in_half_space_counter_for_iteration[index] < points_in_half_space_minimum[index]):
                        points_in_half_space_minimum[index] = points_in_half_space_counter_for_iteration[index]
                        points_in_half_space_counter_for_iteration[index] = 0
                index_error = False
            elif (quadrant_is_terminated[index]):
                if (points_in_half_space_minimum[index] <= min(points_in_half_space_minimum)):
                    return points_in_half_space_minimum[index]


def check_if_obtuse_angle(index, polar_angle_from_h_i_minus_one, polar_angle_from_h_i_plus_one):
    if index == 0 or index == 3:
        if (abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) < 180): 
            return True
    elif index == 1 or index == 2:
        if (abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) > 180): 
            return True
    return False


def get_extracted_elements_count(extracted_elements_counter):
    extracted_elements_for_quadrant_i = [0, 0, 0, 0]
    for index in range(4):
        extracted_elements_for_quadrant_i[index] = extracted_elements_for_quadrant_i[index] + extracted_elements_counter.count(index)
    return extracted_elements_for_quadrant_i


def print_heap(heap):
    for element in heap: 
        print(element, end = ' ')
    print("\n")


def print_points(points):
    for point in points:
        print("Polarwinkel: " , str(point(0)) , ", X: " , str(point(1)) , ", Y: " , str(point(2)))
    print("\n")
    # TODO ich muss depth_i für die einzelnen quadranten ausrechnen. dafür erstelle ich gerade die heaps für die jeweiligen quadranten und muss dann in
    # TODO calculate_depth_i die einzelnen tiefen berechnen
        

