## Faster way for searching  ships allocation

## -------------------------------------------------------------------------------------------------------------------------------------------------
from networkx.algorithms.community import k_clique_communities
from graph.graph_structure import *


## -------------------------------------------------------------------------------------------------------------------------------------------------
def findCliquesSizeK(_G, _k):
    '''
    Find all k-cliques in a graph:
        input:
            _G : nx graph object
            _k : int , size of k-cliques which should been found
        return:
            _all_cliques  : list of vertex lists (cliques)
    '''
    _all_cliques = list()
    ##  "for" per ALL MAXIMAL cliques in _G
    for clique in nx.find_cliques(_G):
        if len(clique) == _k:
            _all_cliques.append(list(sorted(clique)))
        elif len(clique) > _k:
            ##> combination means without permutations, so we have a guaranty,  that mini_clique wouldn't be repeated
            for mini_clique in it.combinations(clique, _k):
                _all_cliques.append(list(sorted(mini_clique)))
    return _all_cliques


## -------------------------------------------------------------------------------------------------------------------------------------------------
def process(_G, _kcc, _k):
    ## create k-clique community graph as a g-subgraph
    kccG = _G.subgraph(sorted(list(_kcc)))
    all_cliques = findCliquesSizeK(kccG, _k)
    return np.array(all_cliques)


## -------------------------------------------------------------------------------------------------------------------------------------------------
def runShipsAllocation(_G, _maxK, shipsQ, _df):
    '''
    Find all cliques in a graph:
        input:
            _G : nx graph object
            _maxK : int , max size of k-cliques which should been found
            shipsQ: int, ships quantity
            _df: dataframe
        return:
            result  : pd.DataFrame result (cliques) with additional attributes
    '''
    all_cliques = []
    for k in range(1, _maxK):
        ## find k-clique communities
        start = time.time()
        if k > 1:
            kcc = list(k_clique_communities(_G, k))
        else:
            kcc = [[x] for x in list(_G.nodes)]
        all_cliques = all_cliques + Parallel(n_jobs=-1)(delayed(process)(_G, _kcc, k) for _kcc in kcc)
        end = time.time()
        print('\nThe search kcc took {:.2f} s to compute. Cliques list len is {}.'.format(end - start,
                                                                                          len(all_cliques[-1])))

    result = pd.DataFrame()
    best_cliques = prepare_clique(all_cliques, shipsQ, _G)
    print(len(best_cliques))
    result = FormatResult(best_cliques, _df, _G)
    return result.sort_values(by=['sumEdgeWeigts', 'shipsCount'], ascending=False)


def prepare_clique(all_cliques, shipsQ, g):
    '''
    Prepare best cliques:
        input:
            all_cliques : all cliques with different sizes
            shipsQ: int, ships quantity
            g : nx graph object
        return:
            result  : list of best cliques
    '''
    all_cliques_with_weights = []
    print(len(all_cliques))
    for k_cliques in all_cliques:
        start = time.time()
        all_cliques_with_weights = all_cliques_with_weights + Parallel(n_jobs=-1, timeout=99999)(
            delayed(process_clique_nx)(clique, g) for clique in reversed(k_cliques))
        end = time.time()
        print('\nThe loop took {:.2f} s to compute. Cliques list len is {}.'.format(end - start, len(k_cliques)))
    all_cliques_with_weights.sort(reverse=True, key=lambda x: x[1])
    best_cliques = choosingBestBins(all_cliques_with_weights, shipsQ)
    return best_cliques


def process_clique_nx(clique, g):
    '''
    Process clique for joblib.Parallel:
        input:
            clique : clique k-size
            g : nx graph object
        return:
            result  : list [clique, sum of edge weights]
    '''
    _edges = nx.get_edge_attributes(g.subgraph(clique), 'weight')
    if len(clique) > 1:
        res = [np.array(clique), sum(_edges.values())]
    else:
        res = [np.array(clique), 0]
    return res


## -------------------------------------------------------------------------------------------------------------------------------------------------
## Choosing the best bins

def choosingBestBins(arr, _shipsQ):
    '''
    Get the subset of best cliques :
        input:
            _result : pd.DataFrame  with all cliques with additional attributes
            _shipsQ : all ships count
        return:
            _result  : pd.DataFrame result short list - best ships allocation
    '''
    _ships = set()  # set(_df.index )
    cliques = []
    for clique in arr:
        _bin = set(clique[0])
        if (len(_ships.intersection(_bin)) == 0):
            _ships = _ships.union(_bin)
            cliques.append(clique[0])
        if (len(_ships) == _shipsQ):
            break
    return cliques

## -------------------------------------------------------------------------------------------------------------------------------------------------
