from global_data import *
from display_results_tkinter import *
from cvrp_solver import cvrp_solver
from flp_solver import flp_solver
from lrp_solver import lrp_solver

if __name__ == '__main__':
    locations = [i for i in range(len(co2_consumption))]
    '''
    solver = cvrp_solver(locations, co2_consumption, truck_capacity, production)
    print("Optimal value", solver.solve_optimal(fairness=True))
    print("Optimal route", solver.routes)
    print("Optimal allocation", solver.cost_allocation)

    print("UFL :")

    solver_ufl = flp_solver(locations,co2_consumption,opening_costs)
    print("Optimal value", solver_ufl.solve_optimal(fairness=True))
    print("Optimal allocation", solver_ufl.cost_allocation)
    '''
    print("LRP :")
    solver_lrp = lrp_solver(locations, opening_costs, co2_consumption, truck_capacity, production)
    print("Optimal value", solver_lrp.solve_optimal(fairness=True))
    print("Optimal allocation", solver_lrp.cost_allocation)

    display_tour_facilities(solver_lrp.opened_facilities, solver_lrp.routes,locations)


    #display_facilities(solver_lrp.opened_facilities,solver_lrp.serving_matrix,locations)
    #display_routes(solver_lrp.routes)
