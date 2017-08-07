#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
from receptive_field_maker import *  # noqa
import graph_tool.centrality
import graph_tool.draw
import numpy as np


GRAPHML_PATH = "./unittest_files/lattice2.graphml"
NODE_SEQUENCE_SIZE = 10
RECEPTIVE_FIELD_SIZE = 6
DISTANCES = [2, 2, 1, 2, 2, 1, 0, 1, 2, 2, 1, 2, 2]


class TestReceptiveFieldMaker(unittest.TestCase):

    def test_constructor(self):
        maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        self.assertTrue(maker)
        self.assertTrue(maker.receptive_field_size == RECEPTIVE_FIELD_SIZE)

    def make_dummy_graph(self):
        graph = graph_tool.Graph(directed=False)
        self.assertTrue(not graph.is_directed())
        graph.add_edge(0, 2)
        graph.add_edge(1, 2)
        graph.add_edge(2, 3)
        graph.add_edge(1, 5)
        e26 = graph.add_edge(2, 6)
        graph.add_edge(3, 7)
        graph.add_edge(4, 5)
        graph.add_edge(5, 6)
        graph.add_edge(6, 7)
        graph.add_edge(7, 8)
        graph.add_edge(5, 9)
        graph.add_edge(6, 10)
        graph.add_edge(7, 11)
        graph.add_edge(10, 12)
        graph.add_edge(9, 10)
        graph.add_edge(10, 11)
        v6 = e26.target()
        return v6, graph

    @staticmethod
    def extend_dummy_graph(graph):
        graph.add_edge(13, 0)
        graph.add_edge(0, 14)
        graph.add_edge(13, 1)
        graph.add_edge(14, 3)
        graph.add_edge(15, 1)
        graph.add_edge(3, 16)
        graph.add_edge(15, 4)
        graph.add_edge(4, 17)
        graph.add_edge(9, 19)
        graph.add_edge(11, 18)
        graph.add_edge(9, 17)
        graph.add_edge(19, 12)
        graph.add_edge(12, 20)
        graph.add_edge(20, 11)
        graph.add_edge(18, 8)
        graph.add_edge(8, 16)
        return graph

    def test_make_receptive_field(self):
        center, graph = self.make_dummy_graph()
        graph = self.extend_dummy_graph(graph)
        self.assertTrue(len(list(graph.vertices())) == 21)

        #
        size = 6
        ans = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        maker = ReceptiveFieldMaker(size)
        rf = maker.make_receptive_field(center)
        self.assertTrue(len(rf) == 13)
        for a, v in zip(ans, rf):
            self.assertTrue(a == graph.vertex_index[v])

        #
        size = 4
        ans = [2, 5, 6, 7, 10]
        maker = ReceptiveFieldMaker(size)
        rf = maker.make_receptive_field(center)
        sorted_rf = sorted(rf, key=lambda x: graph.vertex_index[x])
        self.assertTrue(len(rf) == 5)
        for a, v in zip(ans, sorted_rf):
            self.assertTrue(a == graph.vertex_index[v])

    def test_register_distance(self):
        center, graph = self.make_dummy_graph()
        self.assertTrue(graph.num_vertices() == 13)
        graph = ReceptiveFieldMaker.register_distance(center, graph)
        self.assertTrue(graph.num_vertices() == 13)
        for d, v in zip(DISTANCES, graph.vertices()):
            self.assertTrue(d == graph.vp.distance[v])

    def test_make_temporary_indices(self):
        graph = graph_tool.Graph()
        v0 = graph.add_vertex()
        v1 = graph.add_vertex()
        v2 = graph.add_vertex()

        tmp, tmp_inv = ReceptiveFieldMaker.make_temporary_indices(graph)
        self.assertTrue(tmp[v0] == 0)
        self.assertTrue(tmp[v1] == 1)
        self.assertTrue(tmp[v2] == 2)

        self.assertTrue(tmp_inv[0] == v0)
        self.assertTrue(tmp_inv[1] == v1)
        self.assertTrue(tmp_inv[2] == v2)

    def test_register_edges_to_nauty(self):
        # maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        center, graph = self.make_dummy_graph()
        tmp, tmp_inv = ReceptiveFieldMaker.make_temporary_indices(graph)

        maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        maker.register_edges_to_nauty(tmp, graph)
        # TODO what to do?
        n = maker.nauty_graph.get_vertex_number()
        self.assertTrue(n == 13)

    def test_make_partitioning(self):
        # make a graph
        center, graph = self.make_dummy_graph()

        # calculate distances and make them property of the graph
        graph = ReceptiveFieldMaker.register_distance(center, graph)

        # calculate betweennesses and make them property of the graph
        vbw, _ = graph_tool.centrality.betweenness(graph)
        graph.vp["betweenness"] = graph.new_vertex_property("double")
        graph.vp.betweenness = vbw

        # make temporary indices
        tmp_indices, tmp_inv_indices = ReceptiveFieldMaker.make_temporary_indices(graph)

        # make partitioning
        lab, ptn = ReceptiveFieldMaker.make_partitioning(tmp_indices, graph)
        self.assertTrue(lab == [6, 2, 5, 7, 10, 1, 3, 9, 11, 0, 4, 8, 12])
        self.assertTrue(ptn == [0, 1, 1, 1,  0, 1, 1, 1,  0, 1, 1, 1,  0])

        EPSILON = 1.0e-5
        b2 = graph.vp.betweenness[2]
        b5 = graph.vp.betweenness[5]
        b7 = graph.vp.betweenness[7]
        b10 = graph.vp.betweenness[10]
        self.assertTrue(abs(b2 - b5) < EPSILON and abs(b2 - b7) < EPSILON and abs(b2 - b10) < EPSILON)

        b1 = graph.vp.betweenness[1]
        b3 = graph.vp.betweenness[3]
        b9 = graph.vp.betweenness[9]
        b11 = graph.vp.betweenness[11]
        self.assertTrue(abs(b1 - b3) < EPSILON and abs(b1 - b9) < EPSILON and abs(b1 - b11) < EPSILON)

        b0 = graph.vp.betweenness[0]
        b4 = graph.vp.betweenness[4]
        b8 = graph.vp.betweenness[8]
        b12 = graph.vp.betweenness[12]
        self.assertTrue(abs(b0 - b4) < EPSILON and abs(b0 - b8) < EPSILON and abs(b0 - b12) < EPSILON)

    @staticmethod
    def convert_value(v):
        return 1 if v != 0 else 0

    def test_execute_nauty(self):

        # _/_/_/_/_/_/ Make an input graph _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        # make a graph
        center, graph = self.make_dummy_graph()
        # graph = self.extend_dummy_graph(graph)

        # calculate betweennesses and make them property of the graph
        vbw, _ = graph_tool.centrality.betweenness(graph)
        graph.vp["betweenness"] = graph.new_vertex_property("double")
        graph.vp.betweenness = vbw

        # _/_/_/_/_/_/ Make a receptive field _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        # make an initial receptive field
        maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        rf = maker.make_receptive_field(center)

        # check
        ans = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertTrue(len(rf) == 13)
        for a, v in zip(ans, rf):
            self.assertTrue(a == graph.vertex_index[v])

        # make a subgraph
        receptive_field_graph = graph_tool.GraphView(graph, vfilt=lambda x: x in rf)

        # register distances
        receptive_field_graph = ReceptiveFieldMaker.register_distance(center, receptive_field_graph)

        # check
        for d, v in zip(DISTANCES, rf):
            self.assertTrue(d == receptive_field_graph.vp.distance[v])

        # make temporary indices
        tmp_indices, tmp_inv_indices = ReceptiveFieldMaker.make_temporary_indices(receptive_field_graph)
        maker.register_edges_to_nauty(tmp_indices, receptive_field_graph)

        # make partitioning
        lab, ptn = ReceptiveFieldMaker.make_partitioning(tmp_indices, receptive_field_graph)

        # check
        self.assertTrue(lab == [6, 2, 5, 7, 10, 1, 3, 9, 11, 0, 4, 8, 12])
        self.assertTrue(ptn == [0, 1, 1, 1,  0, 1, 1, 1,  0, 1, 1, 1,  0])

        # execute nauty
        lab, ptn = maker.execute_nauty(lab, ptn)

        # check it
        self.assertTrue(lab == [6, 2, 5, 7, 10, 1, 3, 9, 11, 0, 12, 4, 8])
        self.assertTrue(np.all([0, 1, 1, 1,  0, 1, 1, 1,  0, 1,  1, 1, 0] == [self.convert_value(f) for f in ptn]))

    def test_canonize_receptive_field(self):

        # _/_/_/_/_/_/ Make an input graph _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        # make a graph
        center, graph = self.make_dummy_graph()

        # calculate betweennesses and make them property of the graph
        vbw, _ = graph_tool.centrality.betweenness(graph)
        graph.vp["betweenness"] = graph.new_vertex_property("double")
        graph.vp.betweenness = vbw

        # _/_/_/_/_/_/ Make a receptive field _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        # make an initial receptive field
        maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        rf = maker.make_receptive_field(center)

        # check
        ans = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        self.assertTrue(len(rf) == 13)
        for a, v in zip(ans, rf):
            self.assertTrue(a == graph.vertex_index[v])

        # make a subgraph
        receptive_field_graph = graph_tool.GraphView(graph, vfilt=lambda x: x in rf)

        # register distances
        receptive_field_graph = ReceptiveFieldMaker.register_distance(center, receptive_field_graph)

        # check
        for d, v in zip(DISTANCES, receptive_field_graph.vertices()):
            self.assertTrue(d == receptive_field_graph.vp.distance[v])

        canonized_receptive_field = maker.canonize_receptive_field(receptive_field_graph)
        ans = [6, 2, 5, 7, 10, 1, 3, 9, 11, 0, 12, 4, 8]
        epsilon = 1.0e-05
        ans_bw = [
            0.424242424242,
            0.272727272727,
            0.272727272727,
            0.272727272727,
            0.272727272727,
            0.0530303030303,
            0.0530303030303,
            0.0530303030303,
            0.0530303030303,
            0.0,
            0.0,
            0.0,
            0.0,
        ]

        for i, v in enumerate(canonized_receptive_field):
            self.assertTrue(ans[i] == receptive_field_graph.vertex_index[v])
            self.assertTrue(abs(ans_bw[i] - receptive_field_graph.vp.betweenness[v]) < epsilon)

    def test_make(self):

        # _/_/_/_/_/_/ Make an input graph _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        # make a graph
        center, graph = self.make_dummy_graph()

        # calculate betweennesses and make them property of the graph
        vbw, _ = graph_tool.centrality.betweenness(graph)
        graph.vp["betweenness"] = graph.new_vertex_property("double")
        graph.vp.betweenness = vbw

        # _/_/_/_/_/_/ Make a receptive field _/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/_/

        maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        maker.set_graph(graph)
        rf, rf_graph = maker.make(center)

        self.assertTrue(len(rf) == RECEPTIVE_FIELD_SIZE)
        ans = [6, 2, 5, 7, 10, 1]
        for i, v in enumerate(rf):
            self.assertTrue(ans[i] == v)


if __name__ == "__main__":
    unittest.main()
