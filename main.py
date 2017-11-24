import cplex

# Problem:
# x1 + x2 + ... + xn -> max
# xk + ... + xl <= 1  (ind_set_num times, [k...l] - nodes from idipendent set)
# 0 <= x1 <= 1
# ...
# 0 <= xn <= 1


def solve(nodes: list, ind_sets: list):
    '''
    Construct and solve LP-relaxation of max clique problem
    nodes: list of names of all nodes in graph
    ind_sets: list of independent sets (each as list of nodes names) 
    '''
    # TODO: add costraint xi + xj <= 1, for every pair (i,j) which doesn't connected by edge
    obj = [1.0] * len(nodes)
    upper_bounds = [1.0] * len(nodes)
    # lower bounds are all 0.0 (the default)
    columns_names = ['x{0}'.format(x) for x in nodes]
    right_hand_side = [1.0] * len(ind_sets)
    constraint_names = ['c{0}'.format(x) for x in range(len(ind_sets))]
    constraint_senses = ['L'] * len(ind_sets)

    problem = cplex.Cplex()

    problem.objective.set_sense(problem.objective.sense.maximize)
    problem.variables.add(obj=obj, ub=upper_bounds, names=columns_names)

    constraints = []
    for ind_set in ind_sets:
        constraints.append([['x{0}'.format(x)
                             for x in ind_set], [1.0] * len(ind_set)])

    problem.linear_constraints.add(lin_expr=constraints,
                                   senses=constraint_senses,
                                   rhs=right_hand_side,
                                   names=constraint_names)
    problem.solve()
    print(problem.solution.get_values())


def main():
    nodes = range(1, 10)
    ind_sets = [[1, 2, 3], [3, 4], [7, 8, 9]]
    solve(nodes, ind_sets)


if __name__ == '__main__':
    main()
