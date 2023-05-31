# Genetic Algorithm for Group Combination Optimization
This Python code implements a genetic algorithm to find the best combination of groups from a set of nodes. The goal is to maximize the total weight of the combinations while ensuring that each group has unique nodes and the total number of nodes in each group does not exceed a specified maximum group size.

## Features
* Generates an initial population of individuals, where each individual represents a combination of groups covering all nodes.
* Implements crossover and mutation operations to create new individuals from selected parents.
* Uses a fitness function to evaluate the total weight of each combination and selects the best individuals for the next generation.
* Supports different population sizes, maximum iterations, and maximum group sizes to customize the algorithm.
* Handles negative weights in the total weight calculation.
## Dependencies
This code depends on the following Python packages:

* random
* time
* itertools

Additionally, the code assumes the existence of a module called func.Auxiliary_functions with the following functions:

* ReadSource: Reads data from a source file.
* calcRowOverlap: Calculates the overlap between rows in a dataset.

## Benchmarks

| n  | Time     |
|-----|----------|
| 10  | 0.09 s   |
| 30  | 0.21 s  |
| 80  | 4.87 s   |
| 200 | 30.13 s |

Time fully depends on n_individuals and max_iterations