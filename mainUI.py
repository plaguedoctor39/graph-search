from MIP.pulpsolver import mainPulp
from MIP_itter.ortoolsMIP_iter import mainMIP_iter
from graph.main import mainGraf
from genetic_algorithm.genetic_algo import mainGen
from ACO.aco import mainACO

params = {
    'data': 'data/shipsData200.xlsx',
    'n_rows': 30,
}


def useAco(n_rows, path):
    return mainACO(n_rows, path)


def useGen(n_rows, path):
    return mainGen(n_rows, path)


def useGraph(n_rows, path):
    return mainGraf(n_rows, path)


def useMIP(n_rows, path):
    return mainPulp(n_rows, path)


def useMIP_iter(n_rows, path):
    return mainMIP_iter(n_rows, path)


if __name__ == '__main__':
    result = {'MIP': useMIP(params['n_rows'], params['data']),
              'MIP_iter': useMIP_iter(params['n_rows'], params['data']),
              'Graph': useGraph(params['n_rows'], params['data']),
              'Genetic Algorithm': useGen(params['n_rows'], params['data']),
              'ACO': useAco(params['n_rows'], params['data'])}
    for solution_approach_name, solution in result.items():
        print('------------')
        print(solution_approach_name)
        for key, value in solution.items():
            print(key, value)
