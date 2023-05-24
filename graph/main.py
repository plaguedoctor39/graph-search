import time

from search import *

if __name__ == '__main__':
    _nrows = 30
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
