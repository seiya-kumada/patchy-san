#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import os
from data_preprocessor import *  # noqa
import importlib
import re
import cPickle
import sys

PATTERN = re.compile(r'^[a-zA-Z0-9]+_\d+.graphml$')
PATTERN_2 = re.compile(r'^graph_[0-9]{4}$')


def check_path(path):
    if not os.path.exists(path):
        raise IOError('{} is nod found.'.format(path))


def print_inputs(args):
    print('')
    print('node_sequence_size: {}'.format(args.node_sequence_size))
    print('receptive_field_size: {}'.format(args.receptive_field_size))
    print('num_channels: {}'.format(args.num_channels))
    print('')


def load_graph(path):
    try:
        return graph_tool.load_graph(path)
    except Exception, e:
        print('[EXCEPTION] {}'.format(e))
        return None


def load_graph_(path):
    _, tail = os.path.split(path)
    if PATTERN.match(tail):
        graph = load_graph(path)
        print('[VALID]: {}'.format(path))
        return graph
    else:
        # print('[ERROR] invalid file name: {}'.format(path))
        return None


def load_graph_from_pickle(path):
    _, tail = os.path.split(path)
    if PATTERN_2.match(tail):
        graph = cPickle.load(open(path))
        # print('[VALID]: {}'.format(path))
        return graph
    else:
        print('[ERROR] invalid file name: {}'.format(path))
        return None


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--src_dir_path', help='input: a path to a graphml directory')
        parser.add_argument('--dst_dir_path', help='output: a path to preprocessed directory')
        parser.add_argument('--node_sequence_size', type=int, help='input: the number of nodes in node sequence')
        parser.add_argument('--receptive_field_size', type=int, help='input: the size of a receptive_field')
        parser.add_argument('--channels_module_name', help='input: name of channels module')
        parser.add_argument('--num_channels', type=int, help='input: the number of channels')
        parser.add_argument('--kind', type=int, default=0, help='input: 0 -> .graphml, 1 -> .graph')

        args = parser.parse_args()
        src_dir_path = args.src_dir_path
        dst_dir_path = args.dst_dir_path
        check_path(src_dir_path)

        print_inputs(args)
        if not os.path.exists(dst_dir_path):
            os.mkdir(dst_dir_path)

        channels_module = importlib.import_module(args.channels_module_name)
        preprocessor = DataPreprocessor(args.node_sequence_size, args.receptive_field_size, args.num_channels, channels_module)
        for name in os.listdir(src_dir_path):
            # load a graph
            in_path = os.path.join(src_dir_path, name)
            print('\ninput path: {}'.format(in_path))
            graph = load_graph_(in_path) if args.kind == 0 else load_graph_from_pickle(in_path)
            if graph is None:
                print('graph is None')
                continue

            # print information on the graph
            DataPreprocessor.print_info(name, graph)

            # convert the graph to an input for CNN
            dst = preprocessor.execute(graph)
            print('  output.shape: {}'.format(dst.shape))

            # save it
            head, _ = os.path.splitext(name)
            out_path = os.path.join(dst_dir_path, head)
            np.save(out_path, dst)
            sys.stdout.flush()
    except IOError, e:
        print(e)
