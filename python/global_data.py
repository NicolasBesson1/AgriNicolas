from initialize_data import *
from random import randint

co2_consumption, farm_names, distances, points = initialize_data()

production = [1 for _ in co2_consumption]
truck_capacity = 10
n = len(co2_consumption)
locations = [i for i in range(n)]
opening_costs = [15 for _ in range(n)]
