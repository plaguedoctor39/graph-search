from func.search import *

if __name__ == '__main__':
    _nrows = 80
    _df = ReadSource(_nrows, 'data/shipsData200.xlsx')

    print(_df.head())

    shipsQ = len(_df)

    ## graph preparation
    g = graphPreparation(_df)
    DrawGraph(g)
    maxK = 5
    allBins = runShipsAllocation(g, maxK + 1, shipsQ, _df)
    print(allBins)
