from global_data import *

def individual_rationality(routes):
    global co2_consumption
    ir = [round(co2_consumption[0][j] + co2_consumption[j][0],ndigits=1) for j in range(1,len(co2_consumption))]
    return ir

def marginality(routes):
    m=[0 for _ in range(len(co2_consumption))]
    for route in routes:
        for index in range(1,len(route)-1):
            m[route[index]] = round(co2_consumption[route[index-1]][route[index]] + co2_consumption[route[index]][route[index+1]] - co2_consumption[route[index-1]][route[index+1]],ndigits=1)
    return m[1:]

def route_consumption(route):
    global co2_consumption
    Et=0
    for index in range(len(route)-1):
        Et += co2_consumption[route[index]][route[index+1]]
    return Et
def farm_get_route(routes,i):
    for route in routes:
        if i in route:
            return route
    print("Element not found in routes")
    assert(False)

def ir_method(routes):
    ir=individual_rationality(routes)
    m=marginality(routes)
    n=len(ir)
    assert(len(ir)==len(m))
    allocation=[round((ir[i]/(sum(ir[j] for j in range(n))))*route_consumption(farm_get_route(routes,i)),ndigits=1) for i in range(n)]
    return allocation

def tau_value_method(routes):
    ir=individual_rationality(routes)
    m=marginality(routes)
    n=len(ir)
    allocation=[round( min(ir[i],m[i]) + ((route_consumption(farm_get_route(routes,i))) - (sum(min(ir[j],m[j]) for j in range(n))))*((max(ir[i],m[i]))/(sum(max(ir[j],m[j]) for j in range(n)))), ndigits=1) for i in range(n)]
    return allocation
