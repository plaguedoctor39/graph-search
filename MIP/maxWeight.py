import itertools
import time

from ortools.sat.python import cp_model
from ortools.linear_solver import pywraplp
from itertools import combinations

from func.Auxiliary_functions import ReadSource, calcRowOverlap, getAprovePairs

n_rows = 30
df = ReadSource(n_rows, '../data/shipsData200.xlsx')
ships = [[[i[0], i[1]], calcRowOverlap(i[0], i[1], df)] for i in getAprovePairs(df.index)]

start1 = time.time()


def maximize_total_weight(nodes, weights, min_group_size, max_group_size):
    # Create the solver
    print('Create the solver')
    solver = pywraplp.Solver.CreateSolver('CP-SAT')
    solver.SetNumThreads(10)

    # Create the group variables
    print('Create the group variables')
    group_vars = {}
    for group_size in range(min_group_size, max_group_size + 1):
        for group in combinations(nodes, group_size):
            group_var = solver.BoolVar(f'group({group})')
            group_vars[group] = group_var

    print(f'Length of group variables is - {len(group_vars)}')
    # Add constraints to ensure each node belongs to exactly one group
    print('Add constraints to ensure each node belongs to exactly one group')
    for node in nodes:
        solver.Add(sum(group_vars[group] for group in group_vars if node in group) == 1)

    # Define the objective function
    print('Define the objective function')
    objective = solver.Objective()
    for group, group_var in group_vars.items():
        weight = sum(weights.get((i, j), 0) for i, j in combinations(group, 2))
        objective.SetCoefficient(group_var, weight)
    objective.SetMaximization()

    # Solve the problem
    print('Solve the problem')
    start = time.time()
    status = solver.Solve()
    end = time.time()

    # Process the result
    print('Process the result')
    best_groups = []
    best_total_weight = 0.0
    if status == pywraplp.Solver.OPTIMAL:
        best_total_weight = objective.Value()
        for group, group_var in group_vars.items():
            if group_var.solution_value() > 0.5:
                best_groups.append(group)

    return best_groups, best_total_weight, end - start


# Define weights
print('Define weights')
nodes = list(df.index)
weights = {(i, j): calcRowOverlap(i, j, df) for i, j in combinations(nodes, 2)}

min_group_size = 1  # Change this to the minimum group size
max_group_size = 5  # Change this to the maximum group size

# Find the group combination with the maximum total weight
print('Find the group combination with the maximum total weight')
best_groups, best_total_weight, solve_time = maximize_total_weight(nodes, weights, min_group_size, max_group_size)

# Print the result
print(f"Maximum total weight: {best_total_weight}")
for i, group in enumerate(best_groups):
    group_weight = sum(weights[i, j] for i, j in itertools.combinations(group, 2))
    print(f"Group {i + 1}: {group}, weight: {group_weight}")

end1 = time.time()
print("\nThe solve time is {:.2f} s.".format(solve_time))
print("\nOverall program time is {:.2f} s".format(end1 - start1))
