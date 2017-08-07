#!/usr/bin/env python2.7
# coding:utf-8

import unittest
from dataset import *  # noqa


class TestDataset(unittest.TestCase):

    def test_1(self):
        path = './unittest_files/test.txt'
        root = './unittest_files'
        dataset = Dataset(path, root)
        num_channels = 1
        node_sequence_size = 18
        receptive_field_size = 10
        ans_labels = [1, 0, 1]
        self.assertTrue(3 == len(dataset))
        lower_indices = [17, 20, 14]
        for i in range(len(dataset)):
            graph, label = dataset.get_example(i)
            self.assertTrue(graph.shape == (num_channels, node_sequence_size, receptive_field_size))
            self.assertTrue(ans_labels[i] == label)
            self.assertTrue(np.all(graph[lower_indices[i]:node_sequence_size, :] == 0.0))

    def test_2(self):
        path = './unittest_files/test2.txt'
        root = './unittest_files'
        dataset = Dataset(path, root, offset=1)
        num_channels = 1
        node_sequence_size = 18
        receptive_field_size = 10
        ans_labels = [1, 0, 1]
        self.assertTrue(3 == len(dataset))
        lower_indices = [17, 20, 14]
        for i in range(len(dataset)):
            graph, label = dataset.get_example(i)
            self.assertTrue(graph.shape == (num_channels, node_sequence_size, receptive_field_size))
            self.assertTrue(ans_labels[i] == label)
            self.assertTrue(np.all(graph[lower_indices[i]:node_sequence_size, :] == 0.0))


if __name__ == '__main__':
    unittest.main()
