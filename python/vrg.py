from mip import *
from global_data import *
from tsp import *
from allocation_methods import individual_rationality

def initialize_omega():
    global N
    return [[0,i] for i in N if i != 0]

def c(S):
    global co2_consumption, production, truck_capacity, N
    if sum(production[N.index(i)-1] for i in S) > truck_capacity:
        return 100000
    return tsp_optimal(S)
    

def every_subset_rec(N,i,set_of_subsets,current_subset):
    if i==len(N):
        if current_subset!=[] and current_subset!=[0]:
            set_of_subsets += [current_subset]
    else:
        every_subset_rec(N,i+1,set_of_subsets,current_subset + [N[i]])
        every_subset_rec(N,i+1,set_of_subsets,current_subset)

def every_subset(N):
    set_of_subsets=[]
    every_subset_rec(N,1,set_of_subsets,[0])
    return set_of_subsets



def get_not_omega(all_subsets,omega):
    not_omega=[]
    for S in all_subsets:
        if S not in omega:
            not_omega.append(S)
    return not_omega
      
def master_problem(omega):
    global N
    model = Model(solver_name=CBC)
    
    y = [model.add_var() for _ in N]
    model.objective=maximize(xsum(y[N.index(i)] for i in N))
    model += y[N.index(0)] == 0

    for S in omega:
        model += xsum(y[N.index(i)] for i in S) <= c(S)
        #print(S,c(S))
        
    model.optimize()
    
    if model.num_solutions:
        return [y[N.index(i)].x for i in N]
    else:
        print("Not feasible")
        return None

def core_procedure():
    global N
    #STEP 0
    omega=initialize_omega()

    U=every_subset(N)
    not_omega=get_not_omega(U,omega)
    U.clear()
    #STEP 1
    i=0
    while True:
        #print(i)
        i+=1
        ystar = master_problem(omega)

        PS0k = min(not_omega,key=lambda S:c(S) - sum(ystar[N.index(i)] for i in S))
        not_omega.remove(PS0k)

        if sum(ystar[N.index(i)] for i in PS0k) > c(PS0k):
            omega.append(PS0k)
            if not_omega == []:
                print("Empty core")
                return None
        else:
            print("No coalition is unsatisfied")
            return [round(v,ndigits=1) for v in ystar]
        
        
    
    return [round(v,ndigits=1) for v in ystar]


print(individual_rationality(N))
print(core_procedure())
