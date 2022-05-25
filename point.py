from math import sqrt, atan, pi
from random import randint
from heapq import heappop, heappush, heapify


def create_random_sample_points():
    amount_of_points = int(input("How many points do you want to create? "))
    sample_points = []
    for i in range(amount_of_points):
        sample_point = create_random_sample_point()
        sample_points.append(sample_point)
    return sample_points


def create_random_sample_point():
    x = randint(-5, 5)
    y = randint(-5, 5)
    while x == 0: x = randint(-5, 5)
    while y == 0: y = randint(-5, 5)
    polar_angle = get_polar_angle([x, y])
    return [polar_angle, x, y]


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


def print_points(points):
    for point in points:
        print("Polarwinkel: " , str(point(0)) , ", X: " , str(point(1)) , ", Y: " , str(point(2)))
    print("\n")


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


def calculate_depth_i(quadrants_with_points):
    extracted_elements_for_quadrant_i = []
    index_error = False
    quadrant_i_with_heaps = []
    for index in range(len(quadrants_with_points)): 
        quadrant_i_with_heaps.append(build_heaps_for_quadrant_i(index, quadrants_with_points))
    for index in range(len(quadrants_with_points)):
        try: 
            element_from_h_i_minus_one = heappop(quadrant_i_with_heaps[index][0])
            element_from_h_i_plus_one = heappop(quadrant_i_with_heaps[index][1])
            extracted_elements_for_quadrant_i.append(index)
            if (abs(element_from_h_i_minus_one[0]-element_from_h_i_plus_one[0] > 180)):
                extracted_elements = extracted_elements_for_quadrant_i.count(index)
                scan_depth_i(extracted_elements, index, quadrants_with_points[index], quadrant_i_with_heaps[index])
        except IndexError:
            index_error = True  
        finally:
            if index_error: print("hallo, k:", extracted_elements_for_quadrant_i.count(index))
    # [alles[quadrant1[heap1[punkt]]],[],[],[],]


def scan_depth_i(extracted_elements, index, quadrant_i_with_points, quadrant_i_with_heaps):
    print("get me out von quadrant", index)


def build_heaps_for_quadrant_i(index, quadrants_with_points):
    h_i_minus_one = build_max_heap(quadrants_with_points[(index-1) % 4])
    h_i_plus_one = build_min_heap(quadrants_with_points[(index+1) % 4])
    print("MAX HEAP:", h_i_minus_one)
    print("MIN HEAP:", h_i_plus_one)
    return [h_i_minus_one, h_i_plus_one]


def build_min_heap(quadrant_with_points):
    h_i_plus_one = []
    heapify(h_i_plus_one)
    for point in quadrant_with_points:
        heappush(h_i_plus_one, point)
    return h_i_plus_one


def build_max_heap(quadrant_with_points):
    h_i_minus_one = []
    heapify(h_i_minus_one)
    for point in quadrant_with_points:
        point[0] *= -1
        heappush(h_i_minus_one, point)
    for point in quadrant_with_points:
        point[0] *= -1
    return h_i_minus_one


def print_heap(heap):
    for element in heap: 
        print(element, end = ' ')
    print("\n")





    # TODO ich muss depth_i für die einzelnen quadranten ausrechnen. dafür erstelle ich gerade die heaps für die jeweiligen quadranten und muss dann in
    # TODO calculate_depth_i die einzelnen tiefen berechnen
        

