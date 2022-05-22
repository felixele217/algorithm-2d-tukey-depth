from math import sqrt
from random import randint
from heapq import heapify


class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    @staticmethod
    def create_random_sample_points():
        amount_of_points = int(input("How many points do you want to create? "))
        sample_points = []
        for i in range(amount_of_points):
            sample_point = Point.create_random_sample_point()
            sample_points.append(sample_point)
        return sample_points

    @staticmethod
    def create_random_sample_point():
        x = randint(-10, 10)
        y = randint(-10, 10)
        while x == 0: x = randint(-10, 10)
        while y == 0: y = randint(-10, 10)
        return Point(x, y)
    
    @staticmethod
    def divide_points_into_quadrants(sample_points):
        quadrant_0, quadrant_1, quadrant_2, quadrant_3 = ([] for i in range(4))
        for sample_point in sample_points:
            if sample_point.x > 0 and sample_point.y > 0: 
                quadrant_0.append(sample_point)
            elif sample_point.x < 0 and sample_point.y > 0:
                quadrant_1.append(sample_point)
            elif sample_point.x < 0 and sample_point.y < 0:
                quadrant_2.append(sample_point)
            else:
                quadrant_3.append(sample_point)
        return [quadrant_0, quadrant_1, quadrant_2, quadrant_3]

    @staticmethod
    def calculate_depth_i(quadrants_with_points):
        for i in quadrants_with_points:
            heaps_for_quadrant_i = Point.build_heaps_for_quadrant_i(i, quadrants_with_points)

    @staticmethod
    def build_heaps_for_quadrant_i(i, quadrants_with_points):
        h_i_minus_one = heapify(quadrants_with_points[i-1 % 4])
        h_i_plus_one = heapify(quadrants_with_points[i+1 % 4])
        return [h_i_minus_one, h_i_plus_one]

    # TODO ich muss depth_i für die einzelnen quadranten ausrechnen. dafür erstelle ich gerade die heaps für die jeweiligen quadranten und muss dann in
    # TODO calculate_depth_i die einzelnen tiefen berechnen
        

