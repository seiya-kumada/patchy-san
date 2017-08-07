#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import graph_tool.draw
import graph_tool.centrality
import unittest
from receptive_field_maker import *  # noqa


NODE_SEQUENCE_SIZE = 10
RECEPTIVE_FIELD_SIZE = 6
TOLERANCE = 1.0e-3

RFD_ANSWERS = [
    {"dis": 0, "bwn": 0.127026830638},
    {"dis": 1, "bwn": 0.127026830638},
    {"dis": 1, "bwn": 0.127026830638},
    {"dis": 1, "bwn": 0.116270144421},
    {"dis": 1, "bwn": 0.116270144421},
    {"dis": 2, "bwn": 0.127026830638},
    {"dis": 2, "bwn": 0.116270144421},
    {"dis": 2, "bwn": 0.116270144421},
    {"dis": 2, "bwn": 0.116270144421},
    {"dis": 2, "bwn": 0.116270144421},
    {"dis": 2, "bwn": 0.106816543541},
    {"dis": 2, "bwn": 0.0950786589842},
    {"dis": 2, "bwn": 0.0950786589842},
]
GRAPHML_PATH = "./unittest_files/lattice2.graphml"


class TestReceptiveFieldMaker(unittest.TestCase):

    def test_run(self):

        # if mode == "make":
        #     self.make_dataset(GRAPHML_PATH, 10, 10)
        # else:
        # load .graphml file
        graph = graph_tool.Graph()
        graph.load(GRAPHML_PATH)
        self.assertFalse(graph.is_directed())

        # calculate centrality
        vbw, _ = graph_tool.centrality.betweenness(graph)

        # make it be property
        graph.vp["betweenness"] = graph.new_vertex_property("double")
        graph.vp.betweenness = vbw

        # make a node sequence
        node_sequence = sorted(list(graph.vertices()), key=lambda x: vbw[x], reverse=True)[: NODE_SEQUENCE_SIZE]

        # consider the following vertex
        target = node_sequence[0]

        # make a receptive field
        maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
        maker.set_graph(graph)

        for i in range(10):
            rf, rf_graph = maker.make(target)

            # check it
            for v, a in zip(rf, RFD_ANSWERS[:RECEPTIVE_FIELD_SIZE]):
                self.assertTrue(rf_graph.vp.distance[v] == a["dis"])
                self.assertTrue(abs(rf_graph.vp.betweenness[v] - a["bwn"]) < TOLERANCE)


if __name__ == "__main__":
    unittest.main()
