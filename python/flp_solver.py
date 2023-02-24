from mip import *

class flp_solver:
    def __init__(self, locations, serving_costs, opening_cost):
        self.locations = locations
        self.serving_costs = serving_costs
        self.opening_costs = opening_cost
        self.opened_facilities = None
        self.serving_matrix = None
        self.cost_allocation = None

    #Procedure :
    #Adds to model the FLP constraints
    def add_flp_constraints(self, model, o, s):
        locations = self.locations
        M = sum(self.serving_costs[i][j] for i in locations for j in locations) + sum(self.opening_costs[j] for j in locations)
        #Every location must be served by some facility
        for j in locations:
            model += xsum(s[locations.index(i)][locations.index(j)] for i in locations) == 1

        #If some locations is served by a facility then the facility must open
        for i in locations:
            model += M*o[locations.index(i)] >= xsum(s[locations.index(i)][locations.index(j)] for j in locations)


    def add_efficiency_constraint(self, model, cost, o, s):
        locations = self.locations
        model += xsum(cost[locations.index(j)] for j in locations) == \
                 xsum(o[locations.index(i)]*self.opening_costs[i] for i in locations) + \
                 xsum(s[locations.index(i)][locations.index(j)]*self.serving_costs[i][j]
                      for i in locations
                      for j in locations)

    def add_individual_rationality(self, model, cost):
        locations = self.locations
        for j in locations:
            model += cost[locations.index(j)] <= self.opening_costs[j]

    def add_incremental_contribution(self, model, cost):
        locations = self.locations
        #Compute marginal contributions of each location :

        tmp_solver = flp_solver(locations, self.serving_costs, self.opening_costs)
        optimal = tmp_solver.solve_optimal()

        for j in locations:
            tmp_solver = flp_solver([i for i in locations if i != j], self.serving_costs, self.opening_costs)
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
        locations = self.locations

        model: Model = Model(solver_name=CBC)
        model.verbose = False

        o = [model.add_var(var_type=BINARY) for _ in locations]

        s = [[model.add_var() for _ in locations] for _ in locations]

        if fairness:
            cost = [model.add_var() for _ in locations]

        #Objective : minimize total cost of the tour
        model.objective = minimize(
            xsum(o[locations.index(i)]*self.opening_costs[i] for i in locations)
            + xsum(s[locations.index(i)][locations.index(j)]*self.serving_costs[i][j]
                   for i in locations
                   for j in locations))

        self.add_flp_constraints(model, o, s)

        if fairness:
            self.add_efficiency_constraint(model, cost, o, s)
            self.add_individual_rationality(model, cost)
            self.add_incremental_contribution(model, cost)

        model.optimize()

        #If feasible :
        if model.num_solutions:
            if fairness:
                self.cost_allocation = [round(cost[j].x, ndigits=1) for j in locations]

            self.serving_matrix=[[int(s[locations.index(i)][locations.index(j)].x >= 0.99) for i in locations] for j in locations]
            self.opened_facilities=[int(o[locations.index(i)].x >= 0.99) for i in locations]
            # Return optimal value :
            return round(model.objective_value, ndigits=1)

        else:
            if verbose:
                print('Not feasible')
            assert False
