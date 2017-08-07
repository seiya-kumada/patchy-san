#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
    The purpose of this script is to see computational speed needed for centrality calculation.
"""
import graph_tool.draw
import graph_tool.generation
import graph_tool.centrality
import time
import igraph
import networkx
import networkx.algorithms.centrality

TORUS_PATH = "lattice_periodic.graphml"
LATTICE_PATH = "lattice.graphml"


def make_dataset(torus_path, lattice_path):
    g = graph_tool.generation.lattice([10, 20], periodic=True)
    pos = graph_tool.draw.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    graph_tool.draw.graph_draw(g, pos=pos, output_size=(300, 300), output="lattice_periodict.png")
    g.save(torus_path)

    g = graph_tool.generation.lattice([10, 10])
    pos = graph_tool.draw.sfdp_layout(g, cooling_step=0.95, epsilon=1e-2)
    graph_tool.draw.graph_draw(g, pos=pos, output_size=(300, 300), output="lattice.png")
    g.save(lattice_path)


def use_graph_tool(torus_path, lattice_path, count):
    print("graph-tool")
    g0 = graph_tool.Graph()
    g0.load(torus_path)

    g1 = graph_tool.Graph()
    g1.load(lattice_path)

    start = time.time()
    for _ in range(count):
        v_bw, e_bw = graph_tool.centrality.betweenness(g0)
        v_bw, e_bw = graph_tool.centrality.betweenness(g1)
    end = time.time()
    print("{}[sec]".format((end - start) / count))


def use_igraph(torus_path, lattice_path, count):
    print("igraph")
    g0 = igraph.Graph.Read_GraphML(torus_path)
    g1 = igraph.Graph.Read_GraphML(lattice_path)

    start = time.time()
    for _ in range(count):
        v_bw = g0.betweenness()
        v_bw = g1.betweenness()  # noqa
    end = time.time()
    print("{}[sec]".format((end - start) / count))


def use_networkx(torus_path, lattice_path, count):
    print("networkx")
    g0 = networkx.read_graphml(torus_path)
    g1 = networkx.read_graphml(lattice_path)

    start = time.time()
    for _ in range(count):
        v_bw = networkx.algorithms.centrality.betweenness_centrality(g0)
        v_bw = networkx.algorithms.centrality.betweenness_centrality(g1)  # noqa
    end = time.time()
    print("{}[sec]".format((end - start) / count))


if __name__ == "__main__":
    make_dataset(TORUS_PATH, LATTICE_PATH)
    COUNT = 100

    # graph-tool
    use_graph_tool(TORUS_PATH, LATTICE_PATH, COUNT)

    # igraph
    use_igraph(TORUS_PATH, LATTICE_PATH, COUNT)

    # networkx
    use_networkx(TORUS_PATH, LATTICE_PATH, COUNT)
