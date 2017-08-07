#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
from graph_tool_graph_converter import *  # noqa
import cPickle
import graph_tool.draw
# import graph_tool


class TestGraphToolGraphConverter(unittest.TestCase):

    def convert(self, path):

        converter = GraphToolGraphConverter()
        src_graph = cPickle.load(open(path))
        dst_graph = converter.convert(src_graph)

        num_vertices = sum([1 for v in dst_graph.vertices() if len(dst_graph.get_out_neighbours(v)) != 0])
        self.assertTrue(len(src_graph) == num_vertices)

        for srci, dstv in enumerate(dst_graph.vertices()):
            dst_neighbors = dst_graph.get_out_neighbours(dstv)
            if len(dst_neighbors) == 0:
                continue
            src_neighbors = src_graph[srci]['neighbors']
            dst_label = dst_graph.vp.label[dstv]
            if type(src_graph[srci]['label']) == tuple:
                src_label = src_graph[srci]['label'][0]
            else:
                src_label = int(src_graph[srci]['label'])
            self.assertTrue(src_label == dst_label)
            self.assertTrue(sorted(src_neighbors) == sorted(dst_neighbors))

    def test_convert(self):
        self.convert('./unittest_files/test_graph.pkl')

    def test_convert_2(self):
        self.convert('./unittest_files/test_graph_2.pkl')

    def test_hoge(self):

        path = '/Volumes/Untitled/mac/Data/patchy-san/datasets/for_graph_tool/reddit_subreddit_10K/graph_0100'
        graph = cPickle.load(open(path))
        pos = graph_tool.draw.sfdp_layout(graph, cooling_step=0.5, epsilon=1.0e-2)
        graph_tool.draw.graph_draw(
            graph,
            pos=pos,
            vertex_text=graph.vp.label,
            output_size=(1000, 1000),
            output="./reddit_subreddit_10K.png")
        # g = graph_tool.Graph(directed=False)
        # # vlist = g.add_vertex(5)
        # g.add_edge(0, 2)
        # g.add_edge(2, 3)
        # g.add_edge(3, 4)
        # g.add_edge(4, 5)
        # g.add_edge(5, 0)
        # print(g.num_vertices())

        # for i in range(6):
        #     v = g.vertex(i)
        #     vlist = g.get_out_neighbours(v)
        #     print(i, vlist)


if __name__ == '__main__':
    unittest.main()
