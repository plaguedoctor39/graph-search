## Create graph structure

import networkx as nx
import matplotlib.pyplot as plt
from Auxiliary_functions import *

WEIGHT_THRESHOLD = -1  # Edge will remove if weight  is less than threshold
EDGE_W_COL = 'weight'  # Name of edge weight property


def graphPreparation(_df):
    '''
    Create graph structure:
        input:
            _df  : pd.DataFrame initial ships data
        return:
            _g : nx graph object
    '''
    edges = [[i[0], i[1], calcRowOverlap(i[0], i[1], _df)] for i in getAprovePairs(_df.index)]

    _g = nx.Graph()

    nx.get_edge_attributes(_g, 'weight').values()

    # edges = [i[:2] for i in edges]

    for ii in _df.index:
        _g.add_node(ii)

    for i in edges:
        if i[2] > WEIGHT_THRESHOLD:
            _g.add_edge(i[0], i[1], weight=i[2])

    return _g


def DrawGraph(_g):
    '''
    Drawing nx graph by a shell view
        input:
            _g : nx graph obj
        return:
            nothing
    '''
    # nx.draw_shell(g, with_labels=True, width=g.edges.)
    options = {
    }

    nx.draw_shell(_g
                  , with_labels=True
                  # ,edge_labels=True
                  # ,node_size=[v * 5000 for v in nx.get_node_attributes(G, "nodeWeight").values()]
                  # ,node_size=[v * 1500 for v in dict(g.degree).values()]
                  # ,node_color=[v * 1000 for v in nd.values()]
                  # ,node_cmap=plt.cm.Bnx.get_edge_attributes(g, 'weight').values()lues
                  , width=[e / 1 for e in nx.get_edge_attributes(_g, EDGE_W_COL).values()]
                  # ,edge_cmap=plt.cm.Blues
                  , **options)
    pos = nx.shell_layout(_g)
    nx.draw_networkx_edge_labels(_g, pos, edge_labels=nx.get_edge_attributes(_g, EDGE_W_COL), font_color='red')
