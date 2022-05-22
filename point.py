from math import sqrt
import random


class Point:
    def __init__(self,x_init,y_init):
        self.x = x_init
        self.y = y_init

    def shift(self, x, y):
        self.x += x
        self.y += y

    def __repr__(self):
        return "".join(["Point(", str(self.x), ",", str(self.y), ")"])

    @staticmethod
    def distance(a, b):
        return sqrt((a.x-b.x)**2+(a.y-b.y)**2)

    @staticmethod
    def create_sample_points():
        amount_of_points = int(input("How many points do you want to create? "))
        sample_points = []
        for i in range(amount_of_points):
            Point.create_random_sample_point()

    @staticmethod
    def create_random_sample_point():



# p1 = Point(10, 3)
# p2 = Point(1, 0)

