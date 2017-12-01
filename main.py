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
                _, name, vertices_num, edges_num = line.split()
                print('{0} {1} {2}'.format(name, vertices_num, edges_num))
            elif line.startswith('e'):
                _, v1, v2 = line.split()
                edges.append((v1, v2))
            else:
                continue
        return nx.Graph(edges)


class branch_and_bound:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = self.graph.nodes
        self.ind_sets = []
        self.get_ind_sets()
        self.not_connected = nx.complement(self.graph).edges
        self.init_problem = self.construct_problem()
        self.current_maximum_clique_len = 0

    def get_ind_sets(self):
        strategies = [nx.coloring.strategy_largest_first,
                      nx.coloring.strategy_random_sequential,
                      # nx.coloring.strategy_smallest_last,
                      nx.coloring.strategy_independent_set,
                      nx.coloring.strategy_connected_sequential_bfs,
                      nx.coloring.strategy_connected_sequential_dfs,
                      nx.coloring.strategy_saturation_largest_first]

        for strategy in strategies:
            d = nx.coloring.greedy_color(self.graph, strategy=strategy)
            for color in set(color for node, color in d.items()):
                self.ind_sets.append(
                    [key for key, value in d.items() if value == color])

    def get_branching_variable(self, solution: list):
        return next((index for index, value in enumerate(solution) if not value.is_integer()), None)

    def construct_problem(self):
        '''
        Construct LP-relaxation of max clique problem
        nodes: list of names of all nodes in graph
        ind_sets: list of independent sets (each as list of nodes names)

        Problem\n
        x1 + x2 + ... + xn -> max\n
        xk + ... + xl <= 1  (ind_set_num times, [k...l] - nodes from independent set)\n
        0 <= x1 <= 1\n
        ...\n
        0 <= xn <= 1\n
        xi + xj <= 1, for every pair (i,j) which doesn't connected by edge\n
        '''
        obj = [1.0] * len(self.nodes)
        upper_bounds = [1.0] * len(self.nodes)
        types = 'C' * len(self.nodes)
        # lower bounds are all 0.0 (the default)
        columns_names = ['x{0}'.format(x) for x in self.nodes]
        right_hand_side = [1.0] * \
            (len(self.ind_sets) + len(self.not_connected))
        name_iter = iter(range(len(self.ind_sets) + len(self.nodes)**2))
        constraint_names = ['c{0}'.format(next(name_iter)) for x in range(
            (len(self.ind_sets) + len(self.not_connected)))]
        constraint_senses = ['L'] * \
            (len(self.ind_sets) + len(self.not_connected))

        problem = cplex.Cplex()

        problem.objective.set_sense(problem.objective.sense.maximize)
        problem.variables.add(obj=obj, ub=upper_bounds,
                              names=columns_names, types=types)

        constraints = []
        for ind_set in self.ind_sets:
            constraints.append([['x{0}'.format(x)
                                 for x in ind_set], [1.0] * len(ind_set)])
        for xi, xj in self.not_connected:
            constraints.append(
                [['x{0}'.format(xi), 'x{0}'.format(xj)], [1.0, 1.0]])

        problem.linear_constraints.add(lin_expr=constraints,
                                       senses=constraint_senses,
                                       rhs=right_hand_side,
                                       names=constraint_names)
        return problem

    def branching(self, problem: cplex.Cplex):
        def add_constraint(problem: cplex.Cplex, bv: float, rhs: float):
            problem.linear_constraints.add(lin_expr=[[[bv], [1.0]]],
                                           senses=['E'],
                                           rhs=[rhs],
                                           names=['branch_{0}_{1}'.format(bv, rhs)])
            return problem
        problem.solve()
        solution = problem.solution.get_values()
        print(solution)
        if sum(solution) > self.current_maximum_clique_len:
            bvar = self.get_branching_variable(solution)
            if bvar is None:
                self.current_maximum_clique_len = len(
                    list(filter(lambda x: x == 1.0, solution)))
                print('MAX_LEN',self.current_maximum_clique_len)
                return self.current_maximum_clique_len
            return max(self.branching(add_constraint(cplex.Cplex(problem), bvar, 1.0)),
                       self.branching(add_constraint(cplex.Cplex(problem), bvar, 0.0)))
        return 0

    def solve(self):
        return self.branching(self.init_problem)


def main():
    graph = read_dimacs_graph('./samples/le450_25a.col')
    # bb_max_clique(graph)
    print(branch_and_bound(graph).solve())


if __name__ == '__main__':
    main()
