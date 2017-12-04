## Description
Implementation branch and bound algorithm for maximum clique problem in formulation as an continuous nonconvex optimization problem. 
 
Detailed information in this paper: http://www.dcs.gla.ac.uk/~pat/jchoco/clique/indSetMachrahanish/papers/The%20Maximum%20Clique%20Problem.pdf

## Instructions
This is `Python 3.5.2` realization
Required:
- `NetworkX` library 
- `CPLEX for Python 3.5`

To run script you should specify following parameters:
- `--path` - path to DIMACS-format graph
- `--time` - time limit in seconds

All this graphs are placed in `samples` folder. <br>More of them you can find here: http://mat.gsia.cmu.edu/COLOR/instances.html <br>
Huge ones: http://iridia.ulb.ac.be/~fmascia/maximum_clique/DIMACS-benchmark#detC125.9
