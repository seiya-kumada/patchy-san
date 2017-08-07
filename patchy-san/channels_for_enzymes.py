#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from channels import *  # noqa


class Channels(ChannelsBase):

    # test ok
    def __call__(self, v):
        return self.graph.vp.label[v]


if __name__ == '__main__':
    import graph_tool
    import data_preprocessor

    graph = graph_tool.load_graph('/Volumes/Untitled/mac/Data/graphml/data_graphml/enzymes/enzymes_1.graphml')
    data_preprocessor.DataPreprocessor.print_info('enzymes', graph)

    graph = graph_tool.load_graph('/Volumes/Untitled/mac/Data/graphml/data_graphml/DD/DD_1.graphml')
    data_preprocessor.DataPreprocessor.print_info('DD', graph)

    graph = graph_tool.load_graph('/Volumes/Untitled/mac/Data/graphml/data_graphml/NCI1/NCI1_1.graphml')
    data_preprocessor.DataPreprocessor.print_info('NCI1', graph)

    graph = graph_tool.load_graph('/Volumes/Untitled/mac/Data/graphml/data_graphml/NCI109/NCI109_1.graphml')
    data_preprocessor.DataPreprocessor.print_info('NCI109', graph)
