#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import sys
import graph_tool

# load libnauty_graph
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("../config/settings.conf")
LIBNAUTY_GRAPH_PATH = config.get("settings", "libnauty_graph_path")
sys.path.append(LIBNAUTY_GRAPH_PATH)
import libnauty_graph  # noqa


class ReceptiveFieldMaker(object):

    TOLERANCE = 1.0e-3

    class Comp(object):

        def __init__(self, g):
            self.graph = g

        def __call__(self, vertex):
            return 1.0 / (1 + self.graph.vp.distance[vertex]), self.graph.vp.betweenness[vertex]

    # test ok
    def __init__(self, receptive_field_size):
        self.nauty_graph = libnauty_graph.NautyGraph()
        self.receptive_field_size = receptive_field_size

    def set_graph(self, graph):
        self.graph = graph

    # test ok
    def make_receptive_field(self, vertex):
        n = {vertex}
        ll = {vertex}
        while len(n) < self.receptive_field_size and len(ll) > 0:
            tmp = set()
            for u in ll:
                tmp = tmp.union(set(u.out_neighbours()))
            ll = tmp - n
            n = n.union(ll)
        return list(n)

    # test ok
    @staticmethod
    def register_distance(target, receptive_field_graph):
        path_property = receptive_field_graph.new_vertex_property("int")
        for i, v in enumerate(receptive_field_graph.vertices()):
            # calculate a distance between "v" and "target"
            _, elist = graph_tool.topology.shortest_path(receptive_field_graph, v, target)
            path_property[v] = len(elist)

        # set it to the current graph
        receptive_field_graph.vp["distance"] = path_property
        return receptive_field_graph

    # test ok
    @staticmethod
    def make_temporary_indices(receptive_field_graph):
        tmp_indices = {}
        tmp_inv_indices = {}
        for i, v in enumerate(receptive_field_graph.vertices()):
            tmp_indices[v] = i
            tmp_inv_indices[i] = v
        return tmp_indices, tmp_inv_indices

    # test ok
    def register_edges_to_nauty(self, tmp_indices, receptive_field_graph):
        # set the number of vertices
        num_vertices = receptive_field_graph.num_vertices()
        self.nauty_graph.set_vertex_number(num_vertices)

        # make a graph and register edges to it
        self.nauty_graph.make_graph()

        for i, edge in enumerate(receptive_field_graph.edges()):
            s = edge.source()
            t = edge.target()
            index_s = tmp_indices[s]
            index_t = tmp_indices[t]
            self.nauty_graph.add_edge(index_s, index_t)

    # test ok
    @staticmethod
    def make_partitioning(tmp_indices, receptive_field_graph):
        comp = ReceptiveFieldMaker.Comp(receptive_field_graph)
        sorted_vertices = sorted(list(receptive_field_graph.vertices()), key=comp, reverse=True)
        num_vertices = receptive_field_graph.num_vertices()

        # make patitioning(coloring)
        lab = [0] * num_vertices
        bws = [0] * num_vertices
        dis = [0] * num_vertices
        for i, v in enumerate(sorted_vertices):
            lab[i] = tmp_indices[v]
            bws[i] = receptive_field_graph.vp.betweenness[v]
            dis[i] = receptive_field_graph.vp.distance[v]

        ptn = [0] * num_vertices
        for i in range(num_vertices - 1):
            if abs(bws[i + 1] - bws[i]) < ReceptiveFieldMaker.TOLERANCE and dis[i] == dis[i + 1]:
                ptn[i] = 1
        return lab, ptn

    # test ok
    def execute_nauty(self, lab, ptn):
        # set a partitioning
        self.nauty_graph.set_partition(lab, ptn)

        # run nauty
        self.nauty_graph.execute_dense_nauty()
        lab = self.nauty_graph.get_label()
        ptn = self.nauty_graph.get_ptn()
        return lab, ptn

    # test ok
    def canonize_receptive_field(self, receptive_field_graph):
        # relation between real indices and temporary indices
        tmp_indices, tmp_inv_indices = self.make_temporary_indices(receptive_field_graph)

        self.register_edges_to_nauty(tmp_indices, receptive_field_graph)

        # execute nauty to break ties of labelling
        lab, ptn = self.make_partitioning(tmp_indices, receptive_field_graph)
        lab, ptn = self.execute_nauty(lab, ptn)

        # restore indices to real world
        return [tmp_inv_indices[i] for i in lab]

    # test ok
    def make(self, target):
        # flow from receptive_field_list to receptive_field_graph
        receptive_field_list = self.make_receptive_field(target)
        receptive_field_graph = graph_tool.GraphView(self.graph, vfilt=lambda x: x in receptive_field_list)
        receptive_field_graph = self.register_distance(target, receptive_field_graph)
        canonized_receptive_field = self.canonize_receptive_field(receptive_field_graph)
        return canonized_receptive_field[:self.receptive_field_size], receptive_field_graph


if __name__ == "__main__":
    pass
