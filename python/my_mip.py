from mip import *
import json
from itertools import product
from sys import stdout as out

with open("../data/co2_consumption.json",mode='r') as f:
    co2_consumption=json.load(f)



def every_subset_rec(V,i,set_of_subsets,current_subset):
    if i==len(V):
        if current_subset!=[]:
            set_of_subsets += [current_subset]
    else:
        every_subset_rec(V,i+1,set_of_subsets,current_subset + [V[i]])
        every_subset_rec(V,i+1,set_of_subsets,current_subset)

def every_subset(V):
    set_of_subsets=[]
    every_subset_rec(V,0,set_of_subsets,[])
    return set_of_subsets

nb_locations=len(co2_consumption)
V=[i for i in range(1,nb_locations)]

    



def co2_optimal_allocation(co2_consumption):

    # names of places to visit
    places = ['GSCOP', 'ferme 1', 'ferme 2,', 'ferme 3', 'ferme 4', 'ferme 5']

    # number of nodes and list of vertices
    n, V = len(co2_consumption), set(range(len(co2_consumption)))

    # co2 matrix
    c = [[0 if i == j
          else co2_consumption[i][j-i-1] if j > i
          else co2_consumption[j][i-j-1]
          for j in V] for i in V]

    model = Model(solver_name=CBC)

    # binary variables indicating if arc (i,j) is used on the route or not
    x = [[[model.add_var(var_type=BINARY) for t in V] for j in V] for i in V]

    # continuous variable to prevent subtours: each city will have a
    # different sequential id in the planned route except the first one
    y = [[model.add_var() for i in V] for t in V]

    #co2 allocation

    co2 = [model.add_var() for i in V]

    # objective function: minimize the distance
    model.objective = minimize(xsum(c[i][j]*x[i][j][t] for i in V for j in V for t in V))

    model += xsum(c[i][j]*x[i][j][t] for i in V for j in V for t in V) == xsum(co2[j] for j in range(1,n))

    # constraint : leave each city only once
    for t in V:
        for i in V - {0}:
            model += xsum(x[i][j][t] for j in V - {i}) == xsum(x[j][i][t] for j in V - {i})

    # constraint : enter each city only once

    for i in V - {0}:
        model += xsum(x[j][i][t] for j in V - {i} for t in V) == 1

    for i in V - {0}:
        model += xsum(x[i][j][t] for j in V - {i} for t in V) == 1

    # subtour elimination
    for t in V:
        for (i, j) in product(V - {0}, V - {0}):
            
            if i != j:
                model += y[i][t] - (n+1)*x[i][j][t] >= y[j][t]-n
            
    #Individual stability
    for j in range(1,n):
        model += (co2[j] <= c[0][j] + c[j][0])


    #Symmetry breaking constraints
    for t in V - {n-1}:
        model += xsum(x[0][j][t] for j in V - {0}) >= xsum(x[0][j][t+1] for j in V - {0})
                                                           
    # optimizing
    model.optimize()

    # checking if a solution was found
    if model.num_solutions:
        out.write('route with total co2 consumption of %g found: %s'
                  % (model.objective_value, places[0]))
       
        for t in V:
            out.write('%s' % places[0])
            nc=0
            while True:
                array=[i for i in V if x[nc][i][t].x >= 0.99]
                if array==[]:
                    return None
                nc = array[0]
                out.write(' -> %s' % places[nc])
                if nc == 0:
                    break
            out.write('\n')
        co2_allocation = [co2[j].x for j in range(1,n)]



        print(co2_allocation)
        print(sum(co2_allocation))
    else:
        print('Not feasible')

nb_locations=len(co2_consumption)

#tours,co2_allocation=optimal_co2_allocation(co2_consumption, 10, [1 for _ in range(len(co2_consumption))])

##print(co2_allocation)
##
##for t in tours:
##    print(t)

#print(co2_allocation)

co2_optimal_allocation(co2_consumption)
