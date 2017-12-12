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
MANN_a9.clq|45|918|16|178.044 ms
c-fat200-1.clq|200|1534|12|3037.871 ms
c-fat200-2.clq|200|3235|24|171.062 ms
c-fat500-1.clq|500|4459|14|15152.654 ms
C125.9.clq|125|6963|32|534.007 ms
c-fat200-5.clq|200|8473|58|10119.453 ms
c-fat500-2.clq|500|9139|26|23147.874 ms
brock200_2.clq|200|9876|9|4039.228 ms
p_hat300-1.clq|300|10933|7|18756.434 ms
brock200_3.clq|200|12048|12|3293.948 ms
brock200_4.clq|200|13089|13|3029.496 ms
brock200_1.clq|200|14834|15|2589.552 ms
p_hat300-2.clq|300|21928|20|14269.406 ms
c-fat500-5.clq|500|23191|64|13674.179 ms
C250.9.clq|250|27984|35|2741.839 ms
p_hat500-1.clq|500|31569|7|93783.493 ms
p_hat300-3.clq|300|33390|27|7897.951 ms
c-fat500-10.clq|500|46627|126|10096.493 ms
brock400_3.clq|400|59681|20|17352.028 ms
brock400_1.clq|400|59723|19|18057.946 ms
brock400_4.clq|400|59765|20|17189.867 ms
brock400_2.clq|400|59786|18|17185.887 ms
p_hat500-2.clq|500|62946|27|60446.547 ms
MANN_a27.clq|378|70551|126|674.459 ms
C500.9.clq|500|112332|41|17642.183 ms
brock800_1.clq|800|207505|-|Timeout