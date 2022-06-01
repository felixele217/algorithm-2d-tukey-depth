from math import sqrt, atan, pi
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
    x = randint(-1000, 1000)
    y = randint(-1000, 1000)
    while x == 0: x = randint(-1000, 1000)
    while y == 0: y = randint(-1000, 1000)
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


def calculate_depth_i(quadrants_with_points, heaps_for_quadrants):
    extracted_elements_for_quadrant_i = []
    quadrants_with_terminated_extraction = [] 
    amount_of_points = len(quadrants_with_points[0]) + len(quadrants_with_points[1]) + len(quadrants_with_points[2]) + len(quadrants_with_points[3])
    while len(quadrants_with_terminated_extraction) != 4:
        for index in range(len(quadrants_with_points)):
            try:
                if (index not in quadrants_with_terminated_extraction): 
                    element_from_h_i_minus_one = heappop(heaps_for_quadrants[index][0])# heaps_for_quadrants[index][0][0]
                    heaps_for_quadrants[index][0] = build_max_heap_for_quadrant_i(heaps_for_quadrants[index][0][1:])
                    element_from_h_i_plus_one = heappop(heaps_for_quadrants[index][1])
                    extracted_elements_for_quadrant_i.append(index)
                    if (check_if_obtuse_angle(index, element_from_h_i_minus_one[0], element_from_h_i_plus_one[0])):
                        quadrants_with_terminated_extraction.append(index)
            except IndexError:
                quadrants_with_terminated_extraction.append(index)
    # scan_depth_i(extracted_elements, index, quadrants_with_points[index], heaps_for_quadrants[index])


def check_if_obtuse_angle(index, polar_angle_from_h_i_minus_one, polar_angle_from_h_i_plus_one):
    if index == 0 or index == 3:
        if (abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) < 180): 
            return True
    elif index == 1 or index == 2:
        if (abs(polar_angle_from_h_i_minus_one - polar_angle_from_h_i_plus_one) > 180): 
            return True
    return False


def scan_depth_i(extracted_elements, index, quadrant_i_with_points, quadrant_i_with_heaps):
    print("get me out von quadrant", index)




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
        

