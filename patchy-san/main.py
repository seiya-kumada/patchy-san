#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import graph_tool.collection
import graph_tool.centrality
import graph_tool.draw
from receptive_field_maker import *  # noqa
import numpy as np
import chainer
from chainer import cuda

# load libnauty_graph
import ConfigParser
config = ConfigParser.ConfigParser()
config.read("../config/settings.conf")
LIBNAUTY_GRAPH_PATH = config.get("settings", "libnauty_graph_path")
sys.path.append(LIBNAUTY_GRAPH_PATH)
# import libnauty_graph  # noqa

# xp = cuda.cupy
xp = np
NODE_SEQUENCE_SIZE = 200
RECEPTIVE_FIELD_SIZE = 6
USES_GPU = False


def make_x(batch_size, in_channels, node_sequence, receptive_field_maker):
    # x.shape = (batch_size, in_channels, node_size, rf_size)
    x = np.empty((batch_size, in_channels, len(node_sequence), receptive_field_maker.receptive_field_size)).astype(xp.float32)
    for n, node in enumerate(node_sequence):
        rf, rf_graph = receptive_field_maker.make(node)
        xptr = x[0, :, n, :]
        for i, v in enumerate(rf):
            pos = rf_graph.vp.pos[v].get_array()
            # x[0, :, n, i] = pos
            xptr[:, i] = pos
    return cuda.to_gpu(x) if USES_GPU else x


if __name__ == "__main__":

    print("# load an input graph")
    graph = graph_tool.collection.data["power"]
    print("graph is {}".format("directed" if graph.is_directed() else "undirected"))
    print("the number of vertices:{}".format(graph.num_vertices()))
    print("the number of edges:{}".format(graph.num_edges()))

    print("# calculate centrality")
    bv, ev = graph_tool.centrality.betweenness(graph)
    graph_tool.draw.graph_draw(
        graph,
        pos=graph.vp.pos,
        vertex_fill_color=bv,
        vertex_size=graph_tool.draw.prop_to_size(bv, mi=3, ma=15),
        vorder=bv,
        output="./centrality.png")

    print("# make it be property")
    graph.vp["betweenness"] = graph.new_vertex_property("double")
    graph.vp.betweenness = bv

    print("# decide a node sequence")
    node_sequence = sorted(list(graph.vertices()), key=lambda x: bv[x], reverse=True)[: NODE_SEQUENCE_SIZE]
    receptive_field_maker = ReceptiveFieldMaker(RECEPTIVE_FIELD_SIZE)
    receptive_field_maker.set_graph(graph)

    # weights(dummy)
    # p = 3: feature map size
    # l = 2: channel

    # (1)conv -> (2)conv -> (3)dense -> (4)softmax

    # (1)
    # 16 output channels(feature maps)
    # Rectified unit

    # (2)
    # 8 output channels
    # Stride = 1
    # Field size 10
    # Rectified unit

    # (3)
    # 128 rectified linear units
    # Dropout rate 0.5

    # (5)
    # Hyperparameter:
    #     	the number of epochs
    #             	batch size
    # weights = np.ones((channel_size, RECEPTIVE_FIELD_SIZE))
    # dst_node_sequence = conv(node_sequence, weight)

    print("# make x")
    in_channels = 2
    batch_size = 1
    x = make_x(batch_size, in_channels, node_sequence, receptive_field_maker)

    out_channels = 3
    rf_size = receptive_field_maker.receptive_field_size  # 6

    print("# run the first convolution")
    conv = chainer.links.Convolution2D(
        in_channels=in_channels,
        out_channels=out_channels,
        ksize=(1, rf_size),
        stride=(1, rf_size),
        pad=(0, 0))

    if USES_GPU:
        conv = conv.to_gpu()

    for key in graph.vp.keys():
        print(key)
    y = conv(x)
    assert np.all(y.shape == (batch_size, out_channels, len(node_sequence), 1)), ""
