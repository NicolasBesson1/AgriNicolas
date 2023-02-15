from mip import *
import json
from itertools import product
from sys import stdout as out
from global_data import *
from display_routes_tkinter import *

##def every_subset_rec(V,i,set_of_subsets,current_subset):
##    if i==len(V):
##        if current_subset!=[]:
##            set_of_subsets += [current_subset]
##    else:
##        every_subset_rec(V,i+1,set_of_subsets,current_subset + [V[i]])
##        every_subset_rec(V,i+1,set_of_subsets,current_subset)
##
##def every_subset(V):
##    set_of_subsets=[]
##    every_subset_rec(V,0,set_of_subsets,[])
##    return set_of_subsets

#Add to model the constraints for Vehicle Routing Problem
def add_vrp_constraints(model,V,n,x,y):
    # constraint : if a farm is entered in a tour, then it is left in the same tour
    for t in V:
        for i in V - {0}:
            model += xsum(x[i][j][t] for j in V - {i}) == xsum(x[j][i][t] for j in V - {i})

    # constraint : enter and leave each farm only once

    for i in V - {0}:
        model += xsum(x[j][i][t] for j in V - {i} for t in V) == 1

    for i in V - {0}:
        model += xsum(x[i][j][t] for j in V - {i} for t in V) == 1    

    # subtour elimination
    for t in V:
        for (i, j) in product(V - {0}, V - {0}):
            
            if i != j:
                model += y[i][t] - (n+1)*x[i][j][t] >= y[j][t]-n

    #Symmetry breaking constraints (redundant cuts)
    for t in V - {n-1}:
        model += xsum(x[0][j][t] for j in V - {0}) >= xsum(x[0][j][t+1] for j in V - {0})       

#Adds to model the individual rationality constraint for farmer j
def add_individual_rationality_constraint(model, co2, j):
    global co2_consumption
    model += co2[j] <= co2_consumption[0][j] + co2_consumption[j][0]

#Adds efficiency constraint for farmer j to model (the amount of co2 allocated is equal to the amount of co2 produced)
def add_efficiency_constraint(model, V, co2, x):
    global co2_consumption
    model += xsum(co2[j] for j in V - {0}) == xsum(x[i][j][t]*co2_consumption[i][j] for i in V for j in V for t in V)

#For farmer j, adds marginality constraint
#It computes the difference in co2 consumption of having j in route t and not having j in route t using the variable v[j][i][k][t] which indicates if i is predecessor of j and k successor of j in tour t
#The constraint is activated only if farm j is in tour t (we thus use it[j][t] which indicates if farm j is in tour t)
def add_marginality_constraint(model,V,x,v,co2,m,it,j,M):
    global co2_consumption
    #Marginality
    for t in V:
        model += (m[j] + (1-it[j][t])*M >= (xsum(x[i][j][t]*co2_consumption[i][j] for i in V) + xsum(x[j][i][t]*co2_consumption[j][i] for i in V)) - xsum(v[j][i][k][t]*co2_consumption[i][k] for i in V for k in V))
        model += (co2[j] >= m[j])
                               
#Adds constraints to indicate whether there is a path of size 2 passing through node j from i to k in tour t
def add_path_size_two_constraints(model, V, v, x):
    for i in V:
        for j in V:
            for k in V:
                for t in V:
                    model += v[j][i][k][t] <= x[i][j][t]
                    model += v[j][i][k][t] <= x[j][k][t]
                    model += v[j][i][k][t] >= x[i][j][t] + x[j][k][t] - 1

#Constructs routes using the resulting values for the variables of a model
def construct_routes(V,x):
    routes=[]
    for t in V:
        route=[0]
        nc=0
        while True:
            array=[i for i in V if x[nc][i][t].x >= 0.99]
            if array==[]:
                
                return routes
                #return co2_allocation
            nc = array[0]
            route.append(nc)
            if nc == 0:
                break
        routes.append(route)
    return routes


#Computes a set of routes going through every location in V that minimizes CO2 consumption
def routes_minimum_co2():
    global co2_consumption, farm_names

    places=list(farm_names)
    # number of nodes and list of vertices
    n, V = len(co2_consumption), set(range(len(co2_consumption)))
    
    # co2 matrix
    c = list(co2_consumption)
    model = Model(solver_name=CBC)
    
    # binary variables indicating if arc (i,j) is used in route t or not
    x = [[[model.add_var(var_type=BINARY) for t in V] for j in V] for i in V]
    
    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [[model.add_var() for i in V] for t in V]
    
    #Large constant for M constraints
    M=sum([sum([co2_consumption[i][j] for j in V]) for i in V]) + 1

    #Objective function -> minimize co2 consumption
    model.objective = minimize(xsum(c[i][j]*x[i][j][t] for i in V for j in V for t in V))

    add_vrp_constraints(model,V,n,x,y)


    # optimizing
    model.optimize()

    # checking if a solution was found
    if model.num_solutions:
        routes=[]
        #co2_allocation = [co2[j].x for j in range(1,n)]
        out.write('route with total co2 consumption of %g found:\n'
                  % round((model.objective_value),ndigits=1))
        return construct_routes(V,x)

    else:
        print('Not feasible')
        assert(False)
        return None


def co2_optimal_allocation():
    global co2_consumption, farm_names

    places=list(farm_names)
    # number of nodes and list of vertices
    n, V = len(co2_consumption), set(range(len(co2_consumption)))
    
    # co2 matrix
    c = list(co2_consumption)
    model = Model(solver_name=CBC)
    
    # binary variables indicating if arc (i,j) is used in route t or not
    x = [[[model.add_var(var_type=BINARY) for t in V] for j in V] for i in V]
    
    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [[model.add_var() for i in V] for t in V]

    #Indicates whether farmer i is in tour t
    it = [[model.add_var() for i in V] for t in V]

    #m[i] is the marginality value of farmer i
    m = [model.add_var() for i in V]

    #v[j][i][k][t] = 1 iff x[i][j][t] = 1 and x[j][k][t]
    v = [[[[model.add_var() for _ in V] for _ in V] for _ in V] for _ in V]

    #variable to represent the amount of CO2 allocated to each farm
    co2 = [model.add_var() for i in V]
    
    #Large constant for M constraints
    M=sum([sum([co2_consumption[i][j] for j in V]) for i in V]) + 1

    #Objective function -> minimize co2 consumption
    model.objective = minimize(xsum(c[i][j]*x[i][j][t] for i in V for j in V for t in V))

    add_efficiency_constraint(model,V,co2,x)
    add_vrp_constraints(model,V,n,x,y)

    for t in V:
        for j in V-{0}:
            model += it[j][t] == xsum(x[i][j][t] for i in V)
            
    
    add_path_size_two_constraints(model,V,v,x)
    
    
    for j in range(1,n):
        #Individual rationality
        add_individual_rationality_constraint(model,co2,j)
        add_marginality_constraint(model,V,x,v,co2,m,it,j,M)

    # optimizing
    model.optimize()

    # checking if a solution was found
    if model.num_solutions:
        routes=[]
        #co2_allocation = [co2[j].x for j in range(1,n)]
        out.write('route with total co2 consumption of %g found:\n'
                  % (model.objective_value))
       
        return construct_routes(V,x),[round(co2[j].x,ndigits=1) for j in V - {0}]

    else:
        print('Not feasible')
        assert(False)
        return None    



if __name__=='__main__':
    routes,allocation=co2_optimal_allocation()
    print("The resulting routes are :")
    print(routes)
    print("The resulting allocation is :")
    print(allocation)
    print("If the farmers had been served individually, the co2 allocation would have been :")
    print([round(co2_consumption[0][j] + co2_consumption[j][0],ndigits=1) for j in range(1,len(co2_consumption))])

    
    
    display_routes(routes)
