#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import unittest
import graph_tool
import importlib
import graph_tool.collection
import numpy as np


class TestChannels(unittest.TestCase):

    def test_call(self):
        graph = graph_tool.collection.data['power']
        channels_module = importlib.import_module('channels_for_unittest')
        num_channels = 2
        channels = channels_module.Channels(num_channels)
        channels.set_graph(graph)
        vertices = graph.vertices()
        vertex0 = vertices.next()
        cs = channels(vertex0)
        self.assertTrue((num_channels,) == cs.shape)
        self.assertTrue(np.all(np.abs(cs - np.array([-42.19845128, -93.87027094])) < 1.0e-5))


if __name__ == '__main__':
    unittest.main()
