#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import os
import graph_tool


def load_graph(path):
    try:
        return graph_tool.load_graph(path)
    except Exception:
        # print('  [ERROR] {}'.format(e))
        return None


def calculate_average_number_of_nodes(dir_path):

    s = 0.0
    i = 0
    for name in os.listdir(dir_path):
        # load a graph
        in_path = os.path.join(dir_path, name)
        graph = load_graph(in_path)  # graph_tool.load_graph(in_path)
        if not graph:
            continue

        # print information on the graph
        n = graph.num_vertices()
        s += n
        i += 1

    print('total number of graphs: {}'.format(i))
    print('average number of nodes: {}'.format(s / i))


PATH = '/Volumes/Untitled/mac/Data/graphml/data_graphml/mutag'


if __name__ == '__main__':
    avg = calculate_average_number_of_nodes(PATH)
    print('average: {}'.format(avg))
