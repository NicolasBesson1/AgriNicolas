import json
def initialize_data():
    co2_consumption=None
    distances = None
    points=None
    with open('../data/co2_consumption.json') as f:
        co2_consumption=json.load(f)

    with open('../data/distances.json') as f:
        distances=json.load(f)

    with open('../data/points.json') as f:
        points=json.load(f)

    

    assert(co2_consumption!=None)
    assert(distances!=None)
    assert(points!=None)

    points_coord = [points[key][0] for key in points.keys()]

    farm_names=[key for key in points.keys()]
    
    return co2_consumption, farm_names, distances, points_coord
