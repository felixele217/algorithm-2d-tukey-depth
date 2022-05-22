from math import sqrt
from point import Point


def main(): 
    # 1 create sample points
    sample_points = Point.create_random_sample_points()
    # 2 store sample points in quadrants
    quadrants_with_points = Point.divide_points_into_quadrants(sample_points)
    # 3 calculate depth i for each quadrant and return minimal depth
    depth = Point.calculate_depth_i(quadrants_with_points)


if __name__ == "__main__":
    main()