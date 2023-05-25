import time

from search import *
import cProfile as profile
import pstats

if __name__ == '__main__':
    prof = profile.Profile()
    prof.enable()
    _nrows = 80
    _df = ReadSource(_nrows, 'data/shipsData200.xlsx')

    print(_df.head())

    shipsQ = len(_df)

    ## graph preparation
    g = graphPreparation(_df)
    DrawGraph(g)
    maxK = 5
    start = time.time()
    allBins = runShipsAllocation(g, maxK + 1, shipsQ, _df)
    print(allBins)
    end = time.time()
    print('\nThe program took {:.2f} s to compute. '.format(end - start))
    prof.disable()
    stats = pstats.Stats(prof).strip_dirs().sort_stats("cumtime")
    stats1 = pstats.Stats(prof).strip_dirs().sort_stats("time")
    stats.sort_stats('cumulative').print_stats(10)
    stats1.sort_stats('tottime').print_stats(10)

