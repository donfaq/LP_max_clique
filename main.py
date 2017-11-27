import time
import cplex
import networkx as nx

def timing(f):
    '''
    Measures time of function execution
    '''
    def wrap(*args):
        time1 = time.time()
        ret = f(*args)
        time2 = time.time()
        print('\n{0} function took {1:.3f} ms'.format(
            f.__name__, (time2 - time1) * 1000.0))
        return (ret, '{0:.3f} ms'.format((time2 - time1) * 1000.0))
    return wrap

def read_dimacs_graph(file_path):
    '''
        Parse .col file and return graph object
    '''
    edges = []
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith('c'):  # graph description
                print(*line.split()[1:])
            # first line: p name num_of_vertices num_of_edges
            elif line.startswith('p'):
                p, name, vertices_num, edges_num = line.split()
                print('{0} {1} {2}'.format(name, vertices_num, edges_num))
            elif line.startswith('e'):
                _, v1, v2 = line.split()
                edges.append((v1, v2))
            else:
                continue
        return nx.Graph(edges)

@timing
def solve(nodes: list, ind_sets: list, not_connected: list):
    '''
    Construct and solve LP-relaxation of max clique problem
    nodes: list of names of all nodes in graph
    ind_sets: list of independent sets (each as list of nodes names)

    Problem\n
    x1 + x2 + ... + xn -> max\n
    xk + ... + xl <= 1  (ind_set_num times, [k...l] - nodes from idipendent set)\n
    0 <= x1 <= 1\n
    ...\n
    0 <= xn <= 1\n
    xi + xj <= 1, for every pair (i,j) which doesn't connected by edge\n
    '''
    obj = [1.0] * len(nodes)
    upper_bounds = [1.0] * len(nodes)
    types = 'C' * len(nodes)
    # lower bounds are all 0.0 (the default)
    columns_names = ['x{0}'.format(x) for x in nodes]
    right_hand_side = [1.0] * (len(ind_sets) + len(not_connected))
    name_iter = iter(range(len(ind_sets) + len(nodes)**2))
    constraint_names = ['c{0}'.format(next(name_iter)) for x in range(
        (len(ind_sets) + len(not_connected)))]
    constraint_senses = ['L'] * (len(ind_sets) + len(not_connected))

    problem = cplex.Cplex()

    problem.objective.set_sense(problem.objective.sense.maximize)
    problem.variables.add(obj=obj, ub=upper_bounds,
                          names=columns_names, types=types)

    constraints = []
    for ind_set in ind_sets:
        constraints.append([['x{0}'.format(x)
                             for x in ind_set], [1.0] * len(ind_set)])
    for xi, xj in not_connected:
        constraints.append(
            [['x{0}'.format(xi), 'x{0}'.format(xj)], [1.0, 1.0]])

    problem.linear_constraints.add(lin_expr=constraints,
                                   senses=constraint_senses,
                                   rhs=right_hand_side,
                                   names=constraint_names)

    problem.solve()
    return problem.solution.get_values()


def get_ind_sets(graph):
    ind_sets = []
    strategies = [nx.coloring.strategy_largest_first,
                  nx.coloring.strategy_random_sequential,
                  nx.coloring.strategy_smallest_last,
                  nx.coloring.strategy_independent_set,
                  nx.coloring.strategy_connected_sequential_bfs,
                  nx.coloring.strategy_connected_sequential_dfs,
                  nx.coloring.strategy_saturation_largest_first]
    for strategy in strategies:
        d = nx.coloring.greedy_color(
            graph, strategy=strategy)
        for color in set(color for node, color in d.items()):
            ind_sets.append(
                [key for key, value in d.items() if value == color])
    return ind_sets

def get_branching_variable(solution:list):
    i = 0
    solution = iter(solution)
    while next(solution).is_integer():
        i+=1
    return 'x{0}'.format(i)

def main():
    graph = read_dimacs_graph('.\\samples\\le450_5a.col')
    nodes = graph.nodes
    ind_sets = get_ind_sets(graph)

    print('NODES', len(graph.nodes))
    print('IND_SETS', len(ind_sets))

    solution = solve(nodes, ind_sets, nx.complement(graph).edges)

    print('solution', solution)
    print(get_branching_variable(solution[0]))


if __name__ == '__main__':
    main()
