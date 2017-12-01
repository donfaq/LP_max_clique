import os
import sys
import time
import threading
from contextlib import contextmanager
import _thread
import networkx as nx


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    timer = threading.Timer(seconds, lambda: _thread.interrupt_main())
    timer.start()
    try:
        yield
    except KeyboardInterrupt:
        raise TimeoutException()
    finally:
        timer.cancel()


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


def arguments():
    import argparse
    parser = argparse.ArgumentParser(
        description='Compute maximum clique for a given graph')
    parser.add_argument('--path', type=str, required=True,
                        help='Path to dimacs-format graph file')
    parser.add_argument('--time', type=int, default=60,
                        help='Time limit in seconds')
    return parser.parse_args()
