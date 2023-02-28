
from mip import *


class lrp_solver:

    def __init__(self, locations, location_costs, arc_costs, capacity, demand):
        self.locations = locations
        self.location_costs = location_costs
        self.arc_costs = arc_costs
        self.capacity = capacity
        self.routes = None
        self.demand = demand
        self.cost_allocation = None
        self.objective_function = 0

        self.opened_facilities = None
        self.serving_matrix = None
        self.cost_allocation = None

    def add_lrp_objective_function(self, model, x, o):
        f = self.location_costs
        d = self.arc_costs
        locations = self.locations
        n = len(locations)
        self.objective_function = xsum(o[locations.index(i)] * f[i]
                                       for i in locations) + \
                                  xsum(d[i][j] * x[locations.index(i)][locations.index(j)][t]
                                       for i in locations
                                       for j in locations
                                       for t in range(n))
        model.objective = self.objective_function

    # Procedure :
    # Adds to model the LRP constraints
    def add_lrp_constraints(self, model, x, y, o):
        c = self.arc_costs
        f = self.location_costs
        locations = self.locations

        M = sum(c[i][j] for i in locations for j in locations) + sum(f)
        n = len(locations)

        locations = self.locations
        demand = self.demand

        for j in locations:
            # Either j is a facility or at least an arc enters it
            model += o[locations.index(j)] + xsum(x[locations.index(i)][locations.index(j)][t] for i in locations
                                 for t in range(n) if i != j) >= 1
            # If j is not a facility then exactly one arc enters j
            model += xsum(x[locations.index(i)][locations.index(j)][t] for i in locations for t in range(n)) \
                     <= 1 + M * o[locations.index(j)]
            for t in range(n):
                # If an arc enters location j in tour t, then an arc leaves location j in tour t
                model += xsum(x[locations.index(i)][locations.index(j)][t] for i in locations) \
                         == xsum(x[locations.index(j)][locations.index(i)][t] for i in locations)

        # Capacity constraint (we only count the demand of location j if it is in tour t and if it is not a facility
        for t in range(n):
            model += xsum(demand[j] * (xsum(x[locations.index(i)][locations.index(j)][t]
                                            for i in locations) - o[locations.index(j)]) for j in locations) \
                     <= self.capacity

        # Subtour elimination constraints
        for t in range(n):
            for i in locations:
                for j in locations:
                    if j != i:
                        model += M * o[locations.index(j)] \
                                 + M * o[locations.index(i)] + \
                                 y[locations.index(i)][t] \
                                 - (n + 1) * x[locations.index(i)][locations.index(j)][t] \
                                 >= y[locations.index(j)][t] - n

        #Symmetry breaking constraints :
        #Symmetry breaking constraints (redundant cuts)
        for t in range(n-1):
            model += xsum(x[locations.index(i)][locations.index(j)][t] for j in locations) \
                     >= xsum(x[locations.index(i)][locations.index(j)][t+1] for j in locations)

    def add_efficiency_constraint(self, model, cost):
        locations = self.locations
        model += self.objective_function == xsum(cost[i] for i in locations)

    def add_individual_rationality(self, model, cost):
        locations = self.locations
        for j in locations:
            model += cost[locations.index(j)] <= round(self.location_costs[j], ndigits=1)

    def add_incremental_contribution(self, model, cost):
        # Compute marginal contributions of each location :
        tmp_solver = lrp_solver(self.locations, self.location_costs, self.arc_costs, self.capacity, self.demand)
        optimal = tmp_solver.solve_optimal()

        for j in self.locations:
            tmp_solver = lrp_solver([i for i in self.locations if i != j], self.location_costs, self.arc_costs,
                                    self.capacity, self.demand)
            mj = round(optimal - tmp_solver.solve_optimal(), ndigits=1)
            model += cost[self.locations.index(j)] >= mj

    # Input : self, verbose
    # Output : Minimum cost cycle satisfying the following constraints :
    #           -Every location visited exactly once
    #           -If a location is entered in a tour, it is exited in the same tour
    #           -The demand collected in a tour does not surpass the capacity of the vehicle
    #           -No sub-tours
    #           optional :
    #           -Costs are allocated respecting efficiency, kickback, individual rationality
    #           and incremental contribution

    def construct_routes(self, tours_matrix):
        n = len(self.locations)
        locations = self.locations
        routes = []

        for t in tours_matrix:
            current_location = -1
            #We find a vertex with arc leaving :
            for i in range(len(t)):
                if sum(t[i]) > 0:
                    current_location = i
                    break
            if current_location == -1:
                return routes
            route = [current_location]
            while True:
                for j in range(len(t[current_location])):
                    if t[current_location][j] == 1:
                        route.append(j)
                        current_location = j
                        break
                if current_location == route[0]:
                    routes.append(route)
                    break

        return routes

    def solve_optimal(self, verbose=False, fairness=False):

        locations = self.locations
        n = len(locations)

        model = Model(solver_name=CBC)
        model.verbose = False

        # xijt = 1 if there is an arc from i to j in tour k
        x = [[[model.add_var(var_type=BINARY) for _ in locations] for _ in locations] for _ in locations]
        # Used for subtour elimination
        y = [[model.add_var() for _ in locations] for _ in locations]
        # o[i] = 1 iff we open a facility in location i
        o = [model.add_var(var_type=BINARY) for _ in locations]

        # cost[i] is the allocated cost to player i
        if fairness:
            cost = [model.add_var() for _ in locations]

        # Objective : minimize total cost of the tour
        self.add_lrp_objective_function(model, x, o)

        self.add_lrp_constraints(model, x, y, o)

        if fairness:
            self.add_efficiency_constraint(model, cost)
            self.add_individual_rationality(model, cost)
            self.add_incremental_contribution(model, cost)

        model.optimize()

        # If feasible :
        if model.num_solutions:

            self.opened_facilities = [int(o[locations.index(i)].x >= 0.99) for i in locations]
            # self.construct_routes(x,o)
            if fairness:
                self.cost_allocation = [round(cost[locations.index(j)].x, ndigits=1) for j in locations]
            # Return optimal value :
            tours_matrix = [[[int(x[locations.index(i)][locations.index(j)][t].x >= 0.99)
                            for j in locations] for i in locations] for t in range(n)]
            self.routes = self.construct_routes(tours_matrix)
            return round(model.objective_value, ndigits=1)

        else:
            if verbose:
                print('Not feasible')
            assert False
