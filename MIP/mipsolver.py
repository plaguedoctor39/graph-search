import re

from mip import Model, xsum, BINARY, CBC
from func.Auxiliary_functions import *


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
df = ReadSource(n_rows, '../data/shipsData200.xlsx')
shipsQ = len(df)
N = shipsQ
E = {(i[0] - 1, i[1] - 1): calcRowOverlap(i[0], i[1], df) for i in getAprovePairs(df.index)}
for k, v in E.items():
    if v == 0.0:
        E[k] = 0.1

m = Model("GroupingProblem",solver_name=CBC, sense='maximize')

## variables
x = {(e[0], e[1]): m.add_var(var_type=BINARY, name=f"x({e[0]},{e[1]})") for e in E}

## objective function
m.objective = xsum(x[j[0], j[1]] * j[1] for i, j in enumerate(E.items()))

## constraints: group size
for i in range(N):
    m.add_constr(xsum(x[k, i] for k in range(i - 1, -1, -1)) +
                 xsum(x[i, j] for j in range(i + 1, N)) <= maxC, f"eq0_{i}")

## constraints: check for clique
for i in range(N - 2):
    for j in it.combinations(it.product(range(i, i + 1), range(i + 1, N)), 2):
        m.add_constr(x[j[0]] + x[j[1]] <= x[(j[0][1], j[1][1])] + 1, f"eq1_{j}")

m.optimize()

print("Status:", m.status)
if m.status == "OPTIMAL":
    print("Objective:", m.objective_value)
    print("Decision:")
    for v in m.vars:
        if v.x != 0:
            edge = re.findall(r'\d+', v.name)
            edge = list(map(int, edge))
            edge = [x + 1 for x in edge]
            print(edge)
    edges = [[x + 1 for x in re.findall(r'\d+', v.name)] for v in m.vars if v.x != 0]
    print('len edges - ', len(edges))
    cliques = merge_lists(edges)
    print('Cliques:')
    for clique in cliques:
        print(clique)

end = time.time()
print('\nThe program took {:.2f} s to compute.'.format(end - start))
