from initialize_data import *

co2_consumption, farm_names, distances, points = initialize_data()

production = [1 for _ in co2_consumption[1:]]
truck_capacity = 10
n=len(co2_consumption)
N=[i for i in range(n)]
