from math import sqrt
from point import *


def main(): 
    # 1 create sample points
    sample_points = create_random_sample_points()
    # 2 store sample points in quadrants
    quadrants_with_points = divide_points_into_quadrants(sample_points)
    # 3 calculate depth i for each quadrant and return minimal depth
    depth = calculate_depth_i(quadrants_with_points)


if __name__ == "__main__":
    main()