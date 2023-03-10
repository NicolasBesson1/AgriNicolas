from mip import *

class core_solver:
    def __init__(self, N, c):
        self.N = N
        self.c = c

    def master_problem(self, omega):
        N = self.N
        model = Model(solver_name=CBC)
        model.verbose = 0
        y = [model.add_var() for _ in N]
        model.objective = maximize(xsum(y[N.index(i)] for i in N))

        for S in omega:
            model += xsum(y[N.index(i)] for i in S) <= self.c(S)
            # print(S,c(S))

        model.optimize()

        if model.num_solutions:
            return [y[N.index(i)].x for i in N]
        else:
            print("Not feasible")
            return None

    def initialize_omega(self):
        return [[i] for i in self.N]

    def every_subset_rec(self, i, set_of_subsets, current_subset):
        N = self.N
        if i == len(N):
            if current_subset != []:
                set_of_subsets += [current_subset]
        else:
            self.every_subset_rec(i + 1, set_of_subsets, current_subset + [N[i]])
            self.every_subset_rec(i + 1, set_of_subsets, current_subset)

    def every_subset(self):
        set_of_subsets = []
        self.every_subset_rec(self.N[0], set_of_subsets, [])
        return set_of_subsets

    def get_not_omega(self, all_subsets, omega):
        not_omega = []
        for S in all_subsets:
            if S not in omega:
                not_omega.append(S)
        return not_omega

    def core_procedure(self, verbose=False):
        N = self.N
        c = self.c
        # STEP 0
        omega = self.initialize_omega()

        U = self.every_subset()
        not_omega = self.get_not_omega(U, omega)
        U.clear()
        # STEP 1
        i = 0
        while True:
            # print(i)
            i += 1
            ystar = self.master_problem(omega)
            if ystar == None:
                if verbose:
                    print("Empty core")
                return None

            PS0k = min(not_omega, key=lambda S: c(S) - sum(ystar[N.index(i)] for i in S))
            not_omega.remove(PS0k)

            if sum(ystar[N.index(i)] for i in PS0k) > c(PS0k):
                omega.append(PS0k)
            else:
                if verbose:
                    print("No coalition is unsatisfied")
                return [round(v, ndigits=1) for v in ystar]


