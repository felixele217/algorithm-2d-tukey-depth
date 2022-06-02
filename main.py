from math import sqrt
from point import *


def main(): 
    # 1 create sample points
    sample_points = create_random_sample_points()
    # 2 store sample points in quadrants
    quadrants_with_points = divide_points_into_quadrants(sample_points)
    # 3 calculate depth i for each quadrant and return minimal depth
    heaps_for_quadrants = build_heaps_for_quadrants(quadrants_with_points)
    # for quadrant in heaps_for_quadrants:
    #     print("Heaps: " + str(quadrant))
    extracted_elements_for_quadrants = get_extracted_elemenents_from_heaps(quadrants_with_points, heaps_for_quadrants)
    
    depth = calculate_depth_i(quadrants_with_points, heaps_for_quadrants, extracted_elements_for_quadrants)

    print("Depth: " + str(depth))


if __name__ == "__main__":
    main()