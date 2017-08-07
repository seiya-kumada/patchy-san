#!/usr/bin/env python2.7
# coding:utf-8

from chainer import dataset
import random  # noqa
import numpy as np
import os


class Dataset(dataset.DatasetMixin):

    # test ok
    def __init__(self, path, root, offset=0):

        with open(path) as paths_file:
            pairs = []
            for i, line in enumerate(paths_file):
                pair = line.strip().split()
                if len(pair) != 2:
                    raise ValueError('invalid format at line {} in file {}'.format(i, path))
                pairs.append((pair[0], np.int32(pair[1]) - offset))
            self.pairs = pairs
            self.root = root

    # test ok
    def __len__(self):
        return len(self.pairs)

    # test ok
    def get_example(self, i):
        path, int_label = self.pairs[i]
        full_path = os.path.join(self.root, path)
        graph = np.load(full_path)
        return graph, int_label
