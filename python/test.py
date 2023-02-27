from global_data import *
from display_results_tkinter import *
from cvrp_solver import cvrp_solver
from flp_solver import flp_solver

if __name__ == '__main__':
    locations = [i for i in range(len(co2_consumption))]
    solver = cvrp_solver(locations, co2_consumption, truck_capacity, production)
    print("Optimal value", solver.solve_optimal(fairness=True))
    print("Optimal route", solver.routes)
    print("Optimal allocation", solver.cost_allocation)

    print("UFL :")

    solver_ufl = flp_solver(locations,co2_consumption,opening_costs)
    print("Optimal value", solver_ufl.solve_optimal(fairness=True))
    print("Optimal allocation", solver_ufl.cost_allocation)

    display_facilities(solver_ufl.opened_facilities,solver_ufl.serving_matrix,locations)

    
