import os
import pandas as pd
from utils import *
from main import *


def get_files_size_ordered(dirpath):
    return sorted((os.path.join(basedir, filename)
                   for basedir, dirs, files in os.walk(dirpath) for filename in files),
                  key=os.path.getsize)


def main():
    args = arguments()
    df = pd.DataFrame(
        columns=['file', 'nodes', 'edges', 'clique_size', 'time'])
    files = get_files_size_ordered('test/')
    try:
        for f in files:
            graph = read_dimacs_graph(f)
            try:
                with time_limit(args.time):
                    solution, extime = branch_and_bound(graph).solve()
                    df = df.append({'file': f,
                                    'nodes': graph.number_of_nodes(),
                                    'edges': graph.number_of_edges(),
                                    'clique_size': solution[0],
                                    'time': extime
                                    }, ignore_index=True)
            except Exception:
                df = df.append({'file': f,
                                'nodes': graph.number_of_nodes(),
                                'edges': graph.number_of_edges(),
                                'clique_size': '-',
                                'time': 'Timeout'
                                }, ignore_index=True)
    finally:
        df.to_csv('test_results.csv', index=False, sep='|')


if __name__ == '__main__':
    main()
