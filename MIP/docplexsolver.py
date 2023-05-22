from docplex.mp.model import Model
from func.Auxiliary_functions import *
import time
import re
# import cplex


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

m = Model(name="GroupingProblem")
## variables
x = {(e[0], e[1]): m.binary_var(f"x({e[0]},{e[1]})") for e in list(E)}
## objective function
objs = {0: m.sum(x[j[0][0], j[0][1]] * j[1] for i, j in enumerate(E.items()))}
## constraints :  group size
cons = {
    0: {i: (m.sum(x[(k, i)] for k in range(i - 1, -1, -1)) + m.sum(x[(i, j)] for j in range(i + 1, N))) <= maxC
        for i in range(0, N)}

    ## constraints: check for clique:
    , 1: {j: (x[j[0]] + x[j[1]] <= x[(j[0][1], j[1][1])] + 1) for i in range(N - 2) for j in
          it.combinations(it.product(range(i, i + 1), range(i + 1, N)), 2)}
}

m.print_information()
## add to model
m.maximize(objs[0])
for keys1 in cons:
    for keys2 in cons[keys1]:
        m.add_constraint(cons[keys1][keys2])

print("Model --- \n", m.export_to_string())

result = m.solve(log_output=True)
print("Status --- \n", m.solve_details.status)
if m.solve_details.status == 'optimal':
    print("Objective --- \n", m.objective_value)
    print("Decision --- \n",
          [(variables.name, variables.solution_value) for variables in m.iter_variables() if variables.solution_value != 0])
    edges = []
    for variables in m.iter_variables():
        if variables.solution_value != 0:
            edge = re.findall('[0-9]+', variables.name)
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