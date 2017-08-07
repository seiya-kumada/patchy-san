#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import argparse
import os
import re
import random


def check_path(path):
    if not os.path.exists(path):
        raise IOError('{} is nod found.'.format(path))


def load_labels(path):
    line = open(path).readlines()[0]
    return [int(item) for item in line.split()]


def load_graph_names(dir_path):
    _, basename = os.path.split(dir_path)
    pattern = re.compile(r'{}_(\d+).npy'.format(basename))
    pairs = []
    for name in os.listdir(dir_path):
        m = pattern.match(name)
        if m:
            index = int(m.group(1))
            pairs.append((index, name))
    pairs = sorted(pairs, key=lambda x: x[0])
    return pairs


def split_data(label_path, graph_dir_path):
    labels = load_labels(label_path)
    names = load_graph_names(graph_dir_path)
    pairs = [(name[1], label) for (name, label) in zip(names, labels)]
    random.shuffle(pairs)

    split_num = args.split_num
    length = len(pairs) / split_num
    print('length', length)

    groups = []
    for k, i in enumerate(range(0, len(pairs), length)):
        groups.append(pairs[i: i + length])

    if split_num < len(groups):
        last_group = groups[-1]
        for i, data in enumerate(last_group):
            groups[i].append(data)
        del(groups[-1])

    assert len(groups) == split_num, ''
    return groups


def write_data(outfile, group):
    for pair in group:
        line = '{} {}\n'.format(pair[0], pair[1])
        outfile.write(line)


def save_files(test_index, groups, dst_dir_path):
    test_path = os.path.join(dst_dir_path, 'test.txt')
    train_path = os.path.join(dst_dir_path, 'train.txt')
    test_file = open(test_path, 'w')
    train_file = open(train_path, 'w')
    for i in range(len(groups)):
        if i == test_index:
            write_data(test_file, groups[i])
        else:
            write_data(train_file, groups[i])


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument('--graph_dir_path', help='input: a path to a graphml directory')
        parser.add_argument('--label_path', help='input: a path to a label file')
        parser.add_argument('--split_num', type=int, help='input: a split number')

        args = parser.parse_args()
        graph_dir_path = args.graph_dir_path
        label_path = args.label_path
        check_path(graph_dir_path)
        check_path(label_path)

        groups = split_data(label_path, graph_dir_path)

        # make directories
        for i in range(len(groups)):
            dst_dir_path = os.path.join(graph_dir_path, 'fold_{}'.format(i))
            if not os.path.exists(dst_dir_path):
                os.mkdir(dst_dir_path)
            save_files(i, groups, dst_dir_path)

    except IOError, e:
        print(e)
