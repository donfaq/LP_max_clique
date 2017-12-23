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

## Results
Graph name|#Nodes|#Edges|Found clique length|Time (ms)/Timeout(60s)
---|---|---|---|---
MANN_a9.clq|45|918|16|559.974 ms
c-fat200-1.clq|200|1534|12|2488.318 ms
c-fat200-2.clq|200|3235|24|294.705 ms
c-fat500-1.clq|500|4459|14|27029.180 ms
C125.9.clq|125|6963|34|855937.042 ms
c-fat200-5.clq|200|8473|58|10224.952 ms
c-fat500-2.clq|500|9139|26|7544476.644 ms