import random
import time
from itertools import combinations

from func.Auxiliary_functions import ReadSource, calcRowOverlap


def calculate_group_weight(group, edges):
    total_weight = sum(edges.get((min(i, j), max(i, j)), 0) for i, j in combinations(group, 2))
    return total_weight


def generate_population(nodes, n_individuals, max_group_size):
    population = []
    for _ in range(n_individuals):
        remaining_nodes = set(nodes)
        individual = []
        while remaining_nodes:
            group_size = min(max_group_size, len(remaining_nodes))
            group = random.sample(list(remaining_nodes), group_size)
            individual.append(group)
            remaining_nodes -= set(group)
        population.append(individual)
    return population


def crossover(parent1, parent2, crossover_rate=0.8):
    if random.random() > crossover_rate:
        return parent1, parent2

    # Create copies of parent1 and parent2
    child1 = parent1[:]
    child2 = parent2[:]

    # Find the common nodes between parent1 and parent2
    common_nodes = [node for node in parent1 if node in parent2]

    # Remove common nodes from child1 and child2
    child1 = [node for node in child1 if node not in common_nodes]
    child2 = [node for node in child2 if node not in common_nodes]

    # Shuffle the order of nodes in child1 and child2
    random.shuffle(child1)
    random.shuffle(child2)

    # Combine the common nodes with shuffled child1 and child2
    child1 += common_nodes
    child2 += common_nodes

    return child1, child2


def mutate(individual, edges):
    mutated_individual = []
    remaining_nodes = set([node for group in individual for node in group])

    while remaining_nodes:
        current_group = [random.choice(list(remaining_nodes))]
        remaining_nodes.remove(current_group[0])
        while remaining_nodes and len(current_group) < max_group_size:
            next_node = max(remaining_nodes, key=lambda node: sum(
                edges.get((min(n, node), max(n, node)), 0) for n in current_group))
            remaining_nodes.remove(next_node)
            current_group.append(next_node)
        mutated_individual.append(current_group)
    # print(mutated_individual)
    return mutated_individual


def genetic_algorithm(nodes, edges, n_individuals, max_iterations, max_group_size):
    population = generate_population(nodes, n_individuals, max_group_size)
    best_individual = None
    best_total_weight = float('-inf')

    for _ in range(max_iterations):
        parents = random.sample(population, 2)
        parent1, parent2 = parents
        child1, child2 = crossover(parent1, parent2)
        child1 = mutate(child1, edges)
        child2 = mutate(child2, edges)

        population.append(child1)
        population.append(child2)

        for individual in [child1, child2]:
            # print('individual - ',individual)
            total_weight = sum(calculate_group_weight(group, edges) for group in individual)
            # print('total weight of combination', total_weight)
            if total_weight > best_total_weight:
                print('--------------------')
                print(f'Iteration {_}')
                print('individual - ', individual)
                print('total weight of combination', total_weight)
                best_individual = individual
                best_total_weight = total_weight

        if len(population) > n_individuals:
            population = population[:n_individuals]
    return best_individual, best_total_weight


if __name__ == '__main__':
    start = time.time()

    _nrows = 30
    _df = ReadSource(_nrows, '../data/shipsData200.xlsx')
    nodes = list(_df.index)
    weights = {(i, j): calcRowOverlap(i, j, _df) for i, j in combinations(nodes, 2)}

    n_individuals = 100
    max_iterations = 1000
    max_group_size = 5

    best_individual, best_total_weight = genetic_algorithm(nodes, weights, n_individuals, max_iterations,
                                                           max_group_size)
    print(f"Best group combination: {best_individual}")
    print(f"Best total weight: {best_total_weight}")

    end = time.time()
    print("\nOverall program time is {:.2f} s".format(end - start))
