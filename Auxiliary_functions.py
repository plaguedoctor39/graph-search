## Read dataSource

import pandas as pd
import numpy as np
from joblib import Parallel, delayed

def ReadSource(_nrows, path):
    _df = pd.read_excel(path, skiprows=4, nrows=_nrows)
    _df.set_index('num', inplace=True)
    return _df


## Auxiliary functions

import itertools as it


## -------------------------------------------------------------------------------------------------------------------------------------------------
def calcCross(b1, e1, b2, e2):
    '''
    Calculate duration of cross interval between [b1, e1] and [b2, e2]
        input:
            b1 : 1st interval begin timestamp
            e1 : 1st interval end timestamp
            b2 : 2nd interval begin timestamp
            e2 : 2nd interval end timestamp
        return
            _dur : result as pandas.imedalte
    '''
    i1 = pd.Interval(b1, e1)
    i2 = pd.Interval(b2, e2)
    _dur = 0
    _dur = (e1 - b2) - (((e1 - e2) + abs(e1 - e2)) / 2) - (((b1 - b2) + abs(b1 - b2)) / 2)
    return _dur


## -------------------------------------------------------------------------------------------------------------------------------------------------
def calcRowOverlap(id1, id2, _df):
    '''
    Calculate overlap between 2  timeslots
           input:
            id1 : id 1st interval
            id2 : id 2nd interval
        return
            _dur : result in hours
    '''
    _dur = calcCross(_df.loc[id1]['es'], _df.loc[id1]['ls'], _df.loc[id2]['es'], _df.loc[id2]['ls'])
    return _dur.total_seconds()  / 3600


## -------------------------------------------------------------------------------------------------------------------------------------------------
def removeSameElemtPairs(pairs):
    '''
    Remove pairs with equal 1st and 2nd elements
            input:
            pair : list of pairs
        return
            sorted and shrinked list of pairs
    '''
    mapping = []
    for i in pairs:
        if i[0] != i[1]:
            mapping.append(i)
    return sorted(mapping)


## -------------------------------------------------------------------------------------------------------------------------------------------------
def getAprovePairs(_lst):
    '''
    Preparing all pairs of elements from list, without pairs with equal 1st and 2nd elements
    '''
    return removeSameElemtPairs(sorted(it.combinations_with_replacement(_lst, 2)))


## -------------------------------------------------------------------------------------------------------------------------------------------------
def CalcFitness(_G, _clique):
    '''
    Get clique quality - Fitness Factor
        input:
            _G : nx graph obj
            _clique : list of vertex id's
        return
            _res : list of KPI's [edge with a min weight  in the clique, edge weights, sum of edge weights, len of clique, sum of negative weights, count of negative edges]
    '''
    _edgeWeights = [0]
    _limitEdge = 0
    print(_clique)
    _edges = list(_G.subgraph(_clique).edges(data=True))
    _edges.sort(reverse=False, key=lambda x: x[2]['weight'])
    if len(_clique) > 1:
        _edgeWeights = np.array([e[2]['weight'] for e in np.array(_edges)])
        _limitEdge = _edges[0]
    _res = [_limitEdge, _edgeWeights, sum(_edgeWeights), len(_clique),
            sum([i for i in _edgeWeights if i <= 0]),
            sum([1 for i in _edgeWeights if i < 0])]
    return _res


## -------------------------------------------------------------------------------------------------------------------------------------------------
import types
import time


def FormatResult(_all_cliques, _df, g):
    '''
    Format output for  all cliques:
        input:
            _all_cliques  : list of vertex lists or generator of lists
        return:
            result : sorted pd DataFrame [shipsNums	earlestStart	latestStart	windowLong	limitedShipsPair	sumEdgeWeigts	shipsCount	cntUnMatchedShipsPairs	weightUnMatchedShipsPairs]

    '''
    if isinstance(_all_cliques, types.GeneratorType):
        triad_cliques = [x for x in _all_cliques if len(x) >= 0]
    else:
        triad_cliques = _all_cliques
    _res = []
    start = time.time()
    _res = _res + Parallel(n_jobs=-1)(delayed(do_process)(idx, i, triad_cliques, _df, g) for idx, i in enumerate(triad_cliques))
    end = time.time()
    print('\nThe loop took {:.2f} s to compute. Cliques list len is {}. Clique size is {}'.format(end - start,
                                                                                                  len(triad_cliques),
                                                                                                  len(triad_cliques[
                                                                                                          0])))
    result = pd.DataFrame(
        columns=['shipNums', 'earlestStart', 'latestStart', 'windowLong', 'limitedShipsPair', 'sumEdgeWeigts',
                 'shipsCount', 'cntUnMatchedShipsPairs', 'weightUnMatchedShipsPairs'], data=_res)
    return result.sort_values(by=['sumEdgeWeigts', 'shipsCount'], ascending=False)


## -------------------------------------------------------------------------------------------------------------------------------------------------


def do_process(idx, i, triad_cliques, _df, g):
    return [i, max(_df.loc[triad_cliques[idx]]['es']), min(_df.loc[triad_cliques[idx]]['ls'])] + CalcFitness(g, i)

