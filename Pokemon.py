import math

import networkx as nx

from Position import Position

epsilon = 0.000001


class Pokemon:
    def __init__(self, graph: nx.DiGraph, value=0, type: int = 0, pos: Position = Position(), json_pok=None):
        if json_pok is not None:
            self.load_pok(json_pok)
        else:
            self.value = value  # double value
            self.type = type  # -1 or 1
            self.pos = pos  # Position Class
        self.node_src = None  # src node of  the edge that the Pokemon placed on
        self.node_dest = None  # dst node of the edge that the Pokemon placed on
        self.on_edge_pokemon(graph)

    def load_pok(self, json_pok):  # parse string pokemon to pokemon object
        """Function receives the  pokemon string and load the valuses to the pokemon object """
        self.value = float(json_pok['Pokemon']['value'])
        self.type = int(json_pok['Pokemon']['type'])
        self.pos = Position(location=json_pok['Pokemon']['pos'])

    def on_edge_pokemon(self, graph: nx.DiGraph):
        for i, j, k in graph.edges(data="w"):
            len_edge = graph.nodes[i]['pos'].distance(graph.nodes[j]['pos'])
            pok_to_src = graph.nodes[i]['pos'].distance(self.pos)
            pok_to_dst = graph.nodes[j]['pos'].distance(self.pos)
            if abs((pok_to_src + pok_to_dst) - len_edge) < epsilon:
                if i < j and self.type > 0:
                    self.node_src = i
                    self.node_dest = j
                    break
                elif j < i and self.type < 0:
                    self.node_src = i
                    self.node_dest = j
                    break
