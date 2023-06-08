import time

from graph.search import *
import cProfile as profile
import pstats

def mainGraf(n_rows, path):
    prof = profile.Profile()
    prof.enable()
    _nrows = n_rows
    _df = ReadSource(_nrows, path)

    print(_df.head())

    shipsQ = len(_df)

    ## graph preparation
    g = graphPreparation(_df)
    DrawGraph(g)
    maxK = 5
    start = time.time()
    allBins = runShipsAllocation(g, maxK + 1, shipsQ, _df)
    # print(allBins)
    end = time.time()
    # print('\nThe program took {:.2f} s to compute. '.format(end - start))
    prof.disable()
    stats = pstats.Stats(prof).strip_dirs().sort_stats("cumtime")
    stats1 = pstats.Stats(prof).strip_dirs().sort_stats("time")
    stats.sort_stats('cumulative').print_stats(10)
    stats1.sort_stats('tottime').print_stats(10)
    return {'Objective': sum(allBins['sumEdgeWeigts']), 'Groups': list(allBins['shipNums']), 'Time': '{:.2f} s'.format(end - start)}

