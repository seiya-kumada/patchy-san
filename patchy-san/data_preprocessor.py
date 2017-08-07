#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import graph_tool.centrality
from receptive_field_maker import *  # noqa
import numpy as np


class DataPreprocessor(object):

    # test ok
    def __init__(self, node_sequence_size, receptive_field_size, num_channels, channels_module):
        self.node_sequence_size = node_sequence_size
        self.receptive_field_size = receptive_field_size
        self.channels = channels_module.Channels(num_channels)

    # test ok
    def make_input_for_cnn(self, node_sequence, receptive_field_maker):
        # x.shape = (num_channels, rf_size, node_size)
        x = np.zeros((self.channels.num_channels, self.receptive_field_size, self.node_sequence_size)).astype(np.float32)
        for n, node in enumerate(node_sequence):
            rf, _ = receptive_field_maker.make(node)
            xptr = x[:, :, n]
            for i, v in enumerate(rf):
                xptr[:, i] = self.channels(v)
        return x

    @staticmethod
    def print_info(name, graph):
        num_vertices = graph.num_vertices()
        num_edges = graph.num_edges()
        kind = 'directed' if graph.is_directed() else 'undirected'
        # print('> {}'.format(name))
        print('  num of vertices: {}, num of edges: {}, kind: {}'.format(num_vertices, num_edges, kind))
        vp_keys = [key for key in graph.vp.keys()]
        ep_keys = [key for key in graph.ep.keys()]
        print('  vp.keys: {}'.format(', '.join(vp_keys)))
        print('  ep.keys: {}'.format(', '.join(ep_keys)))

    # test ok
    def execute(self, graph):
        self.channels.set_graph(graph)

        # calculate centrality and make it to be vertex properties
        bv, ev = graph_tool.centrality.betweenness(graph)
        graph.vp['betweenness'] = graph.new_vertex_property('double')
        graph.vp.betweenness = bv

        # decide a node sequence
        num_vertices = graph.num_vertices()
        node_sequence = sorted(
            list(graph.vertices()),
            key=lambda x: bv[x],
            reverse=True)[: min(num_vertices, self.node_sequence_size)]

        receptive_field_maker = ReceptiveFieldMaker(self.receptive_field_size)
        receptive_field_maker.set_graph(graph)

        return self.make_input_for_cnn(node_sequence, receptive_field_maker)
