from global_data import *
from allocation_methods import *
from mip_co2_allocation import *
from display_results_tkinter import *


if __name__=='__main__':
    routes,allocation=co2_optimal_allocation()
    print("The resulting routes are :")
    print(routes)
    print([farm_names[i] for i in routes[0]])
    print("The resulting allocation is :")
    print(allocation)
    print("If the farmers had been served individually, the co2 allocation would have been :")
    print(individual_rationality(routes))
    print("Marginality values for each farm :")
    m=marginality(routes)
    print(m)

    print("Allocation with IR-2 method")
    print(ir_method(routes))
    print("Allocation with tau-value method")
    print(tau_value_method(routes))
    print("Allocation with core procedure")
    print(core_procedure())
    display_routes(routes)
    
