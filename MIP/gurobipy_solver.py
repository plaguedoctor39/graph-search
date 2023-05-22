from gurobipy import *
from func.Auxiliary_functions import *
import time
import re


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
for k, v in E.items():
    if v == 0.0:
        E[k] = 0.1

# Create a new Gurobi model instance
m = Model("GroupingProblem")

# Create variables
x = {(i, j): m.addVar(lb=0, ub=1, vtype=GRB.BINARY, name=f'x({i},{j})') for i, j in E}

# Set objective function
obj = quicksum(E[i, j] * x[i, j] for i, j in E)

# Add constraints
for i in range(N):
    m.addConstr(quicksum(x[k, i] for k in range(i)) + quicksum(x[i, j] for j in range(i + 1, N)) <= maxC, f"eq0_{i}")

for i in range(N - 2):
    for j in it.combinations(it.product(range(i, i + 1), range(i + 1, N)), 2):
        m.addConstr(x[j[0]] + x[j[1]] <= x[(j[0][1], j[1][1])] + 1, f"eq1_{j}")

# Set objective sense
m.modelSense = GRB.MAXIMIZE

# Set time limit
m.setParam(GRB.Param.TimeLimit, 100)

# Optimize model
m.optimize()

# Print solution
if m.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {m.objVal}")
    print("Decision --- \n")
    for v in m.getVars():
        if v.x != 0:
            print(f"{v.varName}: {v.x}")
    edges = []
    for v in m.getVars():
        if v.x != 0:
            edge = re.findall('[0-9]+', v.varName)
            edge = list(map(int, edge))
            edge = [x + 1 for x in edge]
            edges.append(edge)
    print(edges)
    print('len edges - ', len(edges))
    cliques = merge_lists(edges)
    print('Cliques --- \n')
    for clique in cliques:
        print(clique)
# m.write('m.lp')

end = time.time()
print('\nThe program took {:.2f} s to compute.'.format(end - start))
