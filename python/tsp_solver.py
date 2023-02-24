from mip import *

class tsp_solver:
    def __init__(self, locations, costs):
        self.locations = locations
        self.costs = costs
        self.route = None

    #Procedure :
    #Adds to model the TSP constraints
    def add_tsp_constraints(self, model, x, y):
        locations = self.locations
        n = len(locations)
        #Every location entered exactly once
        for i in locations:
            model += xsum(x[locations.index(i)][locations.index(j)] for j in locations if i != j) == 1
        #Every location exited exactly once
        for j in locations:
            model += xsum(x[locations.index(i)][locations.index(j)] for i in locations if i != j) == 1
        #Subtour elimination constraints
        for i in locations[1:]:
            for j in locations[1:]:
                if i != j:
                    model += y[locations.index(i)] - (n + 1) * x[locations.index(i)][locations.index(j)] >= y[locations.index(j)] - n
    #Input : self, verbose
    #Output : Minimum cost cycle satisfying the following constraints :
    #           -Every location visited exactly once
    #           -
    def solve_optimal(self,verbose=False):
        c = self.costs
        locations = self.locations

        model: Model = Model(solver_name=CBC)
        model.verbose = False

        n = len(locations)

        x = [[model.add_var(var_type=BINARY) for _ in locations] for _ in locations]

        y = [model.add_var() for i in locations]

        #Objective : minimize total cost of the tour
        model.objective = minimize(
            xsum(x[locations.index(i)][locations.index(j)] * c[i][j]
                 for i in locations
                 for j in locations))

        self.add_tsp_constraints(model, x, y)

        model.optimize()

        #If feasible :
        if model.num_solutions:
            #Construct route :
            self.route = self.construct_route(x)
            # Return optimal value :
            return round(model.objective_value, ndigits=1)

        else:
            if verbose:
                print('Not feasible')
            assert False

    def construct_route(self, x):
        route = [0]
        n = len(x)
        locations=self.locations
        while True:
            i = route[-1]
            tmp = False
            for j in locations:
                if x[locations.index(i)][locations.index(j)].x >= 0.99:
                    route.append(j)
                    tmp = True
                    break
            if route[-1] == 0 and len(route) > 1:
                return route
            assert tmp
