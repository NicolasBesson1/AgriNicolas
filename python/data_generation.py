from math import sqrt
from random import randint
from global_data import *

def euclidean_distance(x,y):
    return sqrt((x[0]-y[0])**2 + (x[1]-y[1])**2)

def generate_random_points():
    n = 5
    locations = [i for i in range(n)]
    points = []
    for _ in locations:
        point = [randint(0,999),randint(0,999)]
        while point in points:
            point = [randint(0,999),randint(0,999)]
        points.append(point)
    arc_costs = [[euclidean_distance(x,y) for x in points] for y in points]
    opening_costs = [randint(100,1000) for _ in locations]
    truck_capacity = randint(15,50)
    production = [randint(1,5) for _ in locations]
    return points, locations, arc_costs, opening_costs, n, truck_capacity, production
