#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
from data_preprocessor import *  # noqa
import graph_tool.collection
import importlib
import graph_tool.centrality


class TestDataPreprocessor(unittest.TestCase):

    def test_init(self):
        node_sequence_size = 200
        receptive_field_size = 6
        num_channels = 2
        channel_module = importlib.import_module('channels_for_unittest')

        preprocessor = DataPreprocessor(node_sequence_size, receptive_field_size, num_channels, channel_module)

        self.assertTrue(preprocessor.node_sequence_size == node_sequence_size)
        self.assertTrue(preprocessor.receptive_field_size == receptive_field_size)
        self.assertTrue(preprocessor.channels.num_channels == num_channels)

    def test_make_input_for_cnn(self):
        graph = graph_tool.collection.data["power"]
        node_sequence_size = 200
        receptive_field_size = 6
        num_channels = 2
        channel_module = importlib.import_module('channels_for_unittest')

        preprocessor = DataPreprocessor(node_sequence_size, receptive_field_size, num_channels, channel_module)
        preprocessor.channels.set_graph(graph)

        # calculate centrality and make it to be vertex properties
        bv, ev = graph_tool.centrality.betweenness(graph)
        graph.vp['betweenness'] = graph.new_vertex_property('double')
        graph.vp.betweenness = bv

        # decide a node sequence
        node_sequence = sorted(list(graph.vertices()), key=lambda x: bv[x], reverse=True)[: node_sequence_size]

        receptive_field_maker = ReceptiveFieldMaker(receptive_field_size)
        receptive_field_maker.set_graph(graph)

        x = preprocessor.make_input_for_cnn(node_sequence, receptive_field_maker)
        self.assertTrue(x.shape == (num_channels, receptive_field_size, node_sequence_size))
        self.assertTrue(np.all(np.abs(x[:, 0, 0] - np.array([-41.80975723, -94.29560089]))))

    def test_execute(self):
        graph = graph_tool.collection.data["power"]
        node_sequence_size = 200
        receptive_field_size = 6
        num_channels = 2
        channel_module = importlib.import_module('channels_for_unittest')

        preprocessor = DataPreprocessor(node_sequence_size, receptive_field_size, num_channels, channel_module)
        x = preprocessor.execute(graph)
        self.assertTrue(x.shape == (num_channels, receptive_field_size, node_sequence_size))
        self.assertTrue(np.all(np.abs(x[:, 0, 0] - np.array([-41.80975723, -94.29560089]))))

    def test(self):
        graph = graph_tool.load_graph('./unittest_files/mutag_152.graphml')
        node_sequence_size = 18
        receptive_field_size = 10
        num_channels = 1
        channel_module = importlib.import_module('channels_for_mutag')

        preprocessor = DataPreprocessor(node_sequence_size, receptive_field_size, num_channels, channel_module)
        x = preprocessor.execute(graph)
        self.assertTrue((1, receptive_field_size, node_sequence_size) == x.shape)
        # self.assertTrue(np.all(x[14:18, :] == 0.0))


if __name__ == '__main__':
    unittest.main()
