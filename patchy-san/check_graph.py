#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
from preprocess_data_2 import *  # noqa
# import cPickle

if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--src_path', help='input: a path to a .graph file')
        args = parser.parse_args()

        graphs, labels = load_graph(args.src_path)
        print('the number of graphs: {}'.format(len(labels)))
        graph = graphs[4]
        # cPickle.dump(graph, open('./hoge.pkl', 'wb'))
        node = graph[0]
        print('properties of node: {}'.format(node.keys()))
        print('type(node["label"]): {}'.format(type(node['label'])))
        if type(node['label']) is tuple:
            print('type(node["label"][0]): {}'.format(type(node['label'][0])))

        print('type(node["label"]): {}'.format(node['label']))
    except Exception, e:
        print(e)
