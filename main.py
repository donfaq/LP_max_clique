from utils import *
import cplex


class branch_and_bound:
    def __init__(self, graph: nx.Graph):
        self.graph = graph
        self.nodes = self.graph.nodes
        self.ind_sets = []
        self.get_ind_sets()
        self.not_connected = nx.complement(self.graph).edges
        self.problem = self.construct_problem()
        self.current_maximum_clique_len = 0
        self.branch_num = 0

    def get_ind_sets(self):
        strategies = [nx.coloring.strategy_largest_first,
                      nx.coloring.strategy_random_sequential,
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
        return max(list(filter(lambda x: not x[1].is_integer(), enumerate(solution))), 
                    key=lambda x: x[1], default=(None, None))[0]

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
        name_iter = iter(range(len(self.ind_sets) + len(self.nodes) ** 2))
        constraint_names = ['c{0}'.format(next(name_iter)) for x in range(
            (len(self.ind_sets) + len(self.not_connected)))]
        constraint_senses = ['L'] * \
            (len(self.ind_sets) + len(self.not_connected))

        problem = cplex.Cplex()
        problem.set_log_stream(None)
        problem.set_results_stream(None)
        problem.set_warning_stream(None)
        problem.set_error_stream(None)
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

    def branching(self):
        def add_constraint(bv: float, rhs: float, cur_branch: int):
            self.problem.linear_constraints.add(lin_expr=[[[bv], [1.0]]],
                                                senses=['E'],
                                                rhs=[rhs],
                                                names=['branch_{0}'.format(cur_branch)])

        try:
            self.problem.solve()
            solution = self.problem.solution.get_values()
        except cplex.exceptions.CplexSolverError:
            return 0

        if sum(solution) > self.current_maximum_clique_len:
            bvar = self.get_branching_variable(solution)
            if bvar is None:
                self.current_maximum_clique_len = len(
                    list(filter(lambda x: x == 1.0, solution)))
                print('current max clique found:', self.current_maximum_clique_len)
                return self.current_maximum_clique_len, solution
            else:
                self.branch_num += 1
                cur_branch = self.branch_num
                add_constraint(bvar, 1.0, cur_branch)
                branch_1 = self.branching()
                self.problem.linear_constraints.delete(
                    'branch_{0}'.format(cur_branch))
                add_constraint(bvar, 0.0, cur_branch)
                branch_2 = self.branching()
                return max([branch_1, branch_2], 
                            key=lambda x: x[0] if isinstance(x, (list, tuple)) else x)
        return 0

    @timing
    def solve(self):
        return self.branching()


def main():
    args = arguments()
    graph = read_dimacs_graph(args.path)
    try:
        with time_limit(args.time):
            solution, extime = branch_and_bound(graph).solve()

            print('Maximum clique size:', solution[0])
            print('Nodes:', list(index + 1 for index,
                                 value in enumerate(solution[1]) if value == 1.0))
    except TimeoutException:
        print("Timed out!")
        sys.exit(0)


if __name__ == '__main__':
    main()
