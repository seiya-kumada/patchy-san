#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import graph_tool
import graph_tool.draw
import graph_tool.search


class VisitorExample(graph_tool.search.BFSVisitor):

    def __init__(self, name, pred, dist):
        """pred and dist are outputs.
        """
        self.name = name
        self.pred = pred
        self.dist = dist

    def discover_vertex(self, u):
        print("--> {} has been discovered!".format(self.name[u]))

    def examine_vertex(self, u):
        print("{} has been examined...".format(self.name[u]))

    def tree_edge(self, e):
        self.pred[e.target()] = int(e.source())
        self.dist[e.target()] = self.dist[e.source()] + 1


if __name__ == "__main__":

    g = graph_tool.load_graph("search_example.xml")
    for (name, pos) in zip(g.vp["name"], g.vp["pos"]):
        print(name, pos)

    for v in g.vertices():
        index = g.vertex_index[v]
        print("{}->{}".format(index, g.vp.name[v]))

    for e in g.edges():
        index = g.edge_index[e]
        source = e.source()
        target = e.target()
        s_index = g.vertex_index[source]
        t_index = g.vertex_index[target]
        print("{}->{}:{}".format(s_index, t_index, g.ep.weight[e]))


#    graph_tool.draw.graph_draw(
#        g,
#        pos=g.vp["pos"],
#        vertex_text=g.vp["name"],
#        vertex_font_size=12,
#        vertex_shape="double_circle",
#        vertex_fill_color="#729fcf",
#        vertex_pen_width=3,
#        edge_pen_width=g.ep["weight"],
#        output="search_example.png")
#
#    dist = g.new_vertex_property("int")
#    pred = g.new_vertex_property("int64_t")
#    graph_tool.search.bfs_search(g, g.vertex(0), VisitorExample(g.vp["name"], pred, dist))
#    print(dist.a)
#    print(pred.a)
    # I'm now considering how to trace neighborhoods around a target node.
