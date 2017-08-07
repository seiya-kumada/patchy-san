#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
import sys
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("../config/settings.conf")
LIBNAUTY_GRAPH_PATH = config.get("settings", "libnauty_graph_path")
sys.path.append(LIBNAUTY_GRAPH_PATH)
import libnauty_graph  # noqa


class NautyGraphTest(unittest.TestCase):

    def test_process_1(self):
        nauty_graph = libnauty_graph.NautyGraph()

        nauty_graph.set_vertex_number(8)
        nauty_graph.make_graph()

        nauty_graph.add_edge(7, 4)
        nauty_graph.add_edge(4, 0)
        nauty_graph.add_edge(0, 2)
        nauty_graph.add_edge(2, 7)

        nauty_graph.add_edge(0, 5)
        nauty_graph.add_edge(5, 1)
        nauty_graph.add_edge(1, 2)
        nauty_graph.add_edge(2, 5)
        nauty_graph.add_edge(0, 1)

        nauty_graph.add_edge(5, 3)
        nauty_graph.add_edge(3, 6)
        nauty_graph.add_edge(6, 1)

        nauty_graph.execute_dense_nauty()
        label = nauty_graph.get_label()

        answer = [3, 6, 4, 7, 5, 1, 0, 2]
        for a, b in zip(label, answer):
            self.assertTrue(a == b)

    def test_process_2(self):
        nauty_graph = libnauty_graph.NautyGraph()

        nauty_graph.set_vertex_number(8)
        nauty_graph.make_graph()

        nauty_graph.add_edge(7, 4)
        nauty_graph.add_edge(4, 0)
        nauty_graph.add_edge(0, 2)
        nauty_graph.add_edge(2, 7)

        nauty_graph.add_edge(0, 5)
        nauty_graph.add_edge(5, 1)
        nauty_graph.add_edge(1, 2)
        nauty_graph.add_edge(2, 5)
        nauty_graph.add_edge(0, 1)

        nauty_graph.add_edge(5, 3)
        nauty_graph.add_edge(3, 6)
        nauty_graph.add_edge(6, 1)

        src_label = [0, 2, 1, 3, 4, 5, 6, 7]
        ptn = [1, 0, 1, 1, 1, 1, 1, 1]
        nauty_graph.set_partition(src_label, ptn)

        nauty_graph.execute_dense_nauty()
        label = nauty_graph.get_label()

        answer = [0, 2, 3, 6, 4, 7, 5, 1]
        for a, b in zip(label, answer):
            self.assertTrue(a == b)

    def test_process_2_repeatedly(self):
        for i in range(10):
            self.test_process_2()


if __name__ == "__main__":
    unittest.main()
