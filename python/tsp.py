from mip import *
from global_data import *



def tsp_optimal(N):
    global co2_consumption, farm_names

    c=list(co2_consumption)

    
    model = Model(solver_name=CBC)

    n = len(N)
    
    x = [[model.add_var(var_type=BINARY) for _ in N] for _ in N]

    y = [model.add_var() for i in N]
    
    model.objective=minimize(xsum(x[N.index(i)][N.index(j)]*c[i][j] for i in N for j in N))

    for i in N:
        model += xsum(x[N.index(i)][N.index(j)] for j in N if i!=j) == 1
    for j in N:
        model += xsum(x[N.index(i)][N.index(j)] for i in N if i!=j) == 1

    for i in N[1:]:
        for j in N[1:]:
            if i != j:
                model += y[N.index(i)] - (n+1)*x[N.index(i)][N.index(j)] >= y[N.index(j)]-n

    model.optimize()

    if model.num_solutions:
        return round((model.objective_value),ndigits=1)
    
    else:
        print('Not feasible')
        assert(False)
        return -1

    
