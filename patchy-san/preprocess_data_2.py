#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import pickle
import numpy as np
import progressbar
from graph_tool_graph_converter import *  # noqa
import cPickle
import os


def load_graph(src_path):
    try:
        data = pickle.load(open(src_path))
        graph_data = data['graph']
        labels = np.array(data['labels'], dtype=np.float)
        if 'proteins' in src_path:
            labels = labels[0]
        return graph_data, labels
    except TypeError:
        raise Exception('invalid file')


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--src_path', help='input: a path to a .graph file')
        parser.add_argument('--dst_dir_path', help='output: a path to a directory for graph files(.pkl)')
        parser.add_argument('--dst_label_path', help='output: a path to a file for label file(.pkl)')

        args = parser.parse_args()

        src_path = args.src_path
        if not os.path.exists(src_path):
            raise Exception('not found {}'.format(src_path))

        dst_dir_path = args.dst_dir_path
        if not os.path.exists(dst_dir_path):
            os.mkdir(dst_dir_path)

        graphs, labels = load_graph(src_path)

        num_labels = len(labels)
        print('> the number of graphs: {}'.format(num_labels))
        cPickle.dump(labels, open(args.dst_label_path, 'wb'))

        bar = progressbar.ProgressBar(num_labels).start()
        converter = GraphToolGraphConverter()
        print(num_labels)
        for i in range(num_labels):
            gt_graph = converter.convert(graphs[i])
            path = os.path.join(dst_dir_path, 'graph_{0:04d}'.format(i))
            cPickle.dump(gt_graph, open(path, 'wb'))
            bar.update(i + 1)
    except Exception, e:
        print('Error: {}'.format(e))
