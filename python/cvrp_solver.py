from mip import *

class cvrp_solver:
    def __init__(self, locations, costs, capacity, demand):
        self.locations = locations
        self.costs = costs
        self.capacity = capacity
        self.routes = None
        self.demand = demand
        self.cost_allocation = None

    #Procedure :
    #Adds to model the TSP constraints
    def add_cvrp_constraints(self, model, x, y, it):
        locations = self.locations
        demand = self.demand

        n = len(locations)

        #Every location exited exactly once
        for i in locations:
            if i != 0:
                model += xsum(x[locations.index(i)][locations.index(j)][t]
                              for j in locations
                              for t in range(n) if i != j) == 1

        #Every location entered exactly once
        for j in locations:
            if j != 0:
                model += xsum(x[locations.index(i)][locations.index(j)][t] for i in locations
                              for t in range(n)
                              if i != j and j != 0) == 1

        #If a location is entered in tour t, it is also exited in tour t
        for t in range(n):
            for j in locations:
                model += xsum(x[locations.index(i)][locations.index(j)][t] for i in locations if i != j) \
                         == xsum(x[locations.index(j)][locations.index(i)][t] for i in locations if i != j)

        #A location is visited in tour t if it is entered in tour t
        for t in range(n):
            for j in locations:
                if j != 0:
                    model += it[locations.index(j)][t] == xsum(x[locations.index(i)][locations.index(j)][t]
                                                               for i in locations
                                                               if i != j)

        #Capacity constraint :

        for t in range(n):
            model += xsum(demand[j-1]*it[locations.index(j)][t] for j in locations if j != 0) <= self.capacity

        #Subtour elimination constraints
        for t in range(n):
            for i in locations:
                for j in locations:
                    if i != j and i != 0 and j != 0:
                        model += y[locations.index(i)][t] - (n + 1) * x[locations.index(i)][locations.index(j)][t] \
                                 >= y[locations.index(j)][t] - n

        #Symmetry breaking constraints :
        #Symmetry breaking constraints (redundant cuts)
        for t in range(n-1):
            model += xsum(x[locations.index(0)][locations.index(j)][t] for j in locations if j != 0) \
                     >= xsum(x[locations.index(0)][locations.index(j)][t+1] for j in locations if j != 0)

    def add_efficiency_constraint(self, model, cost, x):
        locations = self.locations
        n = len(locations)
        model += xsum(cost[locations.index(j)] for j in locations if j != 0) == \
                 xsum(self.costs[i][j]*x[locations.index(i)][locations.index(j)][t] for i in locations for j in locations
                      for t in range(n))
    def add_individual_rationality(self, model, cost):
        locations = self.locations

        for j in locations:
            if j != 0:
                model += cost[locations.index(j)] <= round(self.costs[0][j] + self.costs[j][0], ndigits=1) + 0.1

    def add_incremental_contribution(self, model, cost):
        locations = self.locations
        #Compute marginal contributions of each location :

        tmp_solver = cvrp_solver(locations, self.costs, self.capacity, self.demand)
        optimal = tmp_solver.solve_optimal()

        for j in locations:
            if j != 0:
                tmp_solver = cvrp_solver([i for i in locations if i != j], self.costs, self.capacity, self.demand)
                mj = round(optimal - tmp_solver.solve_optimal(), ndigits=1)
                model += cost[locations.index(j)] >= mj




    #Input : self, verbose
    #Output : Minimum cost cycle satisfying the following constraints :
    #           -Every location visited exactly once
    #           -If a location is entered in a tour, it is exited in the same tour
    #           -The demand collected in a tour does not surpass the capacity of the vehicle
    #           -No sub-tours
    #           (optional)
    #           -Costs are allocated respecting efficiency, kickback, individual rationality
    #           and incremental contribution
    def solve_optimal(self,verbose = False, fairness = False):
        c = self.costs
        locations = self.locations

        model: Model = Model(solver_name=CBC)
        model.verbose = False

        x = [[[model.add_var(var_type=BINARY) for _ in locations] for _ in locations] for _ in locations]

        y = [[model.add_var() for _ in locations] for _ in locations]

        it = [[model.add_var() for _ in locations] for _ in locations]

        if fairness:
            cost = [model.add_var() for _ in locations]

        #Objective : minimize total cost of the tour
        model.objective = minimize(
            xsum(x[locations.index(i)][locations.index(j)][locations.index(t)] * c[i][j]
                 for i in locations
                 for j in locations
                 for t in locations))

        self.add_cvrp_constraints(model, x, y, it)

        if fairness:
            self.add_efficiency_constraint(model, cost, x)
            self.add_individual_rationality(model, cost)
            self.add_incremental_contribution(model, cost)

        model.optimize()

        #If feasible :
        if model.num_solutions:
            #Construct route :
            self.routes = self.construct_routes(x)
            if fairness:
                self.cost_allocation = [0.0] + [round(cost[j].x, ndigits=1) for j in locations if j != 0]
            # Return optimal value :
            return round(model.objective_value, ndigits=1)

        else:
            if verbose:
                print('Not feasible')
            assert False

    def construct_routes(self, x):
        n = len(x)
        locations = self.locations
        routes = []
        for t in locations:
            route = [0]
            while True:
                i = route[-1]
                tmp = False
                for j in locations:
                    if x[locations.index(i)][locations.index(j)][t].x >= 0.99:
                        route.append(j)
                        tmp = True
                        break
                if route[-1] == 0 and len(route) > 1:
                    break
                if not tmp:
                    return routes
            routes.append(route)
