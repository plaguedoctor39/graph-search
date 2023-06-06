from itertools import combinations
import time

from func.Auxiliary_functions import ReadSource, calcRowOverlap, ReadSourceCargo, prepareCargoData

start = time.time()
_nrows = 30
# _df = ReadSource(_nrows, '../data/shipsData200.xlsx')
_df = ReadSourceCargo('../data/cargo.csv')
nodes, weights, cargoWeight = prepareCargoData(_df)
# nodes = list(_df.index)
# weights = {(i, j): calcRowOverlap(i, j, _df) for i, j in combinations(nodes, 2)}

import random


class Ant:
    def __init__(self, nodes, edges):
        self.nodes = nodes[:]
        self.edges = edges
        self.group = []

    def find_group(self):
        while self.nodes:
            current_group = [self.nodes.pop(random.randrange(len(self.nodes)))]
            while self.nodes and len(current_group) < max_group_size:
                next_node = max(self.nodes, key=lambda node: sum(
                    self.edges.get((min(n, node), max(n, node)), 0) for n in current_group))
                # self.nodes.remove(next_node)
                # current_group.append(next_node)
                if check_group(current_group + [next_node]):  # Add check_group constraint for cargo.csv
                    self.nodes.remove(next_node)
                    current_group.append(next_node)
                else:
                    break
            self.group.append(current_group)


def aco(nodes, edges, n_ants, max_iterations):
    best_group = None
    best_total_weight = float('-inf')

    for _ in range(max_iterations):
        ants = [Ant(nodes, edges) for _ in range(n_ants)]
        for ant in ants:
            ant.find_group()
            total_weight = 0
            for group in ant.group:
                group_weight = sum(edges.get((min(i, j), max(i, j)), 0) for i in group for j in group if i != j) / 2
                total_weight += group_weight
            if total_weight > best_total_weight:
                print('--------------------')
                print(f'Iteration {_}')
                print('individual - ', ant.group)
                print('total weight of combination', total_weight)
                best_total_weight = total_weight
                best_group = ant.group
    return best_group, best_total_weight

def check_group(group):
    group_weight = sum(cargoWeight[i] for i in group)
    if group_weight > max_group:
        return False
    return True

nodes = list(set([node for edge in weights.keys() for node in edge]))

n_ants = 10
max_iterations = 100
max_group_size = 2
max_group = 100

best_group, best_total_weight = aco(nodes, weights, n_ants, max_iterations)

print(f"Best group: {best_group}")
print(f"Best total weight: {best_total_weight}")

end = time.time()
print("\nOverall program time is {:.2f} s".format(end - start))
