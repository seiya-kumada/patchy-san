#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
    The purpose of this script is to see computational speed for centrality calculation.
"""
import graph_tool.draw
import graph_tool.generation
import graph_tool.centrality

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
    g = graph_tool.Graph()
    g.load(lattice_path)

    v_bw, e_bw = graph_tool.centrality.betweenness(g)
    g.vp['betweenness'] = g.new_vertex_property('double')
    g.vp.betweenness = v_bw

    for v in g.vertices():
        print(g.vp.betweenness[v])


if __name__ == "__main__":
    make_dataset(TORUS_PATH, LATTICE_PATH)
    COUNT = 1

    # graph-tool
    use_graph_tool(TORUS_PATH, LATTICE_PATH, COUNT)
