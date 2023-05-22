##
## Interpretation as a MIP problem
from func.Auxiliary_functions import *
import time
import re
import pulp as lp

print(lp.listSolvers(onlyAvailable=True))
# def merge_lists(lists):
#     result = []
#     while len(lists) > 0:
#         current = lists.pop(0)
#         shared = False
#         # print(current)
#         for i in range(len(result)):
#             if set(current) & set(result[i]):
#                 # print(f'set current {set(current)} == {set(result[i])}')
#                 shared = True
#                 result[i] = list(set(current + result[i]))
#                 break
#         if not shared:
#             result.append(current)
#     return result

def merge_lists(lists):
    result = []
    while len(lists) > 0:
        current = lists.pop(0)
        merged_lists = [current]
        i = 0
        while i < len(merged_lists):
            for j in range(len(lists)):
                if set(merged_lists[i]) & set(lists[j]):
                    merged_lists.append(lists.pop(j))
                    break
            i += 1
        merged_list = []
        for lst in merged_lists:
            merged_list += lst
        merged_set = set(merged_list)
        new_list = sorted(list(merged_set))
        result.append(new_list)
    return result


start = time.time()
maxC = 4
n_rows = 30
df = ReadSource(n_rows, 'data/shipsData200.xlsx')
shipsQ = len(df)
N = shipsQ
E = {(i[0] - 1, i[1] - 1): calcRowOverlap(i[0], i[1], df) for i in getAprovePairs(df.index)}
for k,v in E.items():
    if v == 0.0:
        E[k] = 0.1

# print(E)
# import pulp as op
#
# ispmodel = "y"
# solve = "y"
# dispresult = "y"
#
# m = op.LpProblem("GroupingProblem", op.LpMaximize)
# ## variables
# x = {(e[0], e[1]): op.LpVariable(f"x({e[0]},{e[1]})", 0, 1, op.LpBinary) for e in list(E)}
# ## objective function
# objs = {0: sum(x[j[0][0], j[0][1]] * j[1] for i, j in enumerate(E.items()))}
# print(objs)
# ## constraints
# cons = {
#     0: {i: (sum(x[(k, i)] for k in range(i - 1, -1, -1)) + sum(x[(i, j)] for j in range(i + 1, N)) <= maxK, f"eq0_{i}")
#         for i in range(0, N)}
# }
# print(cons)
# ## add ro model
# m += objs[0]
# for keys1 in cons:
#     for keys2 in cons[keys1]: m += cons[keys1][keys2]
# # print(cons)
# print("Model --- \n", m)
# if solve == "y":
#     result = m.solve(op.PULP_CBC_CMD(timeLimit=None, threads=10, timeMode='elapsed'))
#     print("Status --- \n", op.LpStatus[result])
#     if dispresult == "y" and op.LpStatus[result] == 'Optimal':
#         print("Objective --- \n", op.value(m.objective))
#         print("Decision --- \n",
#               [(variables.name, variables.varValue) for variables in m.variables() if variables.varValue != 0])
#         edges = []
#         for variables in m.variables():
#             if variables.varValue != 0:
#                 edge = re.findall('[0-9]+', variables.name)
#                 edge = list(map(int, edge))
#                 edge = [x + 1 for x in edge]
#                 edges.append(edge)
#         print(edges)
#         print(len(edges))
#         cliques = merge_lists(edges)
#         print('Cliques --- \n')
#         for clique in cliques:
#             print(clique)


import itertools as it
from ortools.linear_solver import pywraplp

ispmodel = "y"
solve = "y"
dispresult = "y"

# Create a new solver instance
solver = pywraplp.Solver.CreateSolver('CBC')
# solver = pywraplp.Solver('LinearProgrammingExample', pywraplp.Solver.GLPK_LINEAR_PROGRAMMING)
# solver.set_time_limit(10000) # Set timeout to 10 seconds

# solver.SetNumThreads(10)

## variables
x = {}
for e in list(E):
    x[e[0], e[1]] = solver.IntVar(0, 1, f'x({e[0]},{e[1]})')

## objective function
objs = {0: sum(x[j[0][0], j[0][1]] * j[1] for i, j in enumerate(E.items()))}

## constraints :  group size
cons = {}
for i in range(0, N):
    cons[i] = solver.Constraint(-solver.infinity(), maxC)
    for k in range(i - 1, -1, -1):
        cons[i].SetCoefficient(x[k, i], 1)
    for j in range(i + 1, N):
        cons[i].SetCoefficient(x[i, j], 1)

## constraints: check for clique:
for i in range(N - 2):
    for j in it.combinations(it.product(range(i, i + 1), range(i + 1, N)), 2):
        cons[j] = solver.Constraint(-solver.infinity(), 1)
        cons[j].SetCoefficient(x[j[0][0], j[0][1]], 1)
        cons[j].SetCoefficient(x[j[1][0], j[1][1]], 1)
        cons[j].SetCoefficient(x[j[0][1], j[1][1]], -1)

## add objective function to solver
solver.Maximize(objs[0])
# solver.Solve()

if solve == "y":
    result = solver.Solve()
    if dispresult == "y" and result == pywraplp.Solver.OPTIMAL:
        print("Objective --- \n", solver.Objective().Value())
        print("Decision --- \n",
              [(variables.name(), variables.solution_value()) for variables in solver.variables() if variables.solution_value() != 0])

        edges = []
        for variables in solver.variables():
            if variables.solution_value() != 0:
                edge = re.findall('[0-9]+', str(variables.name))
                edge = list(map(int, edge))
                edge = [x + 1 for x in edge]
                edges.append(edge)
        print(edges)
        print('len edges - ', len(edges))
        cliques = merge_lists(edges)
        print('Cliques --- \n')
        for clique in cliques:
            print(clique)
end = time.time()
print('\nThe program took {:.2f} s to compute.'.format(end - start))
