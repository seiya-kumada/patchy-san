#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import graph_tool


class GraphToolGraphConverter(object):

    def convert(self, src_graph):
        ps = set()
        ls = []
        for i, src_node in src_graph.items():
            neighbors = src_node['neighbors']
            label = src_node['label']
            value = None
            if type(label) is tuple:
                value = label[0]
            else:
                value = int(label) if label != '' else -1
            ls.append((i, value))

            for j in neighbors:
                p = tuple(sorted([i, j]))
                ps.add(p)  # no duplication!!

        # add edges to a graph
        dst_graph = graph_tool.Graph(directed=False)
        for p in ps:
            dst_graph.add_edge(p[0], p[1])

        # add labels to a graph
        label_property = dst_graph.new_vertex_property('int')
        for i, label in ls:
            v = dst_graph.vertex(i)
            label_property[v] = label
        dst_graph.vp['label'] = label_property
        return dst_graph


if __name__ == '__main__':
    pass
