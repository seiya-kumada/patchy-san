#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import json
import os
import numpy as np

DIR_NAME = 'fold_{}'


if __name__ == '__main__':
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--root_dir_path", help="input: set a path to a root directory")
        parser.add_argument("--fold_num", type=int, help="input: the number of fold: [0,9]")

        args = parser.parse_args()
        if args.fold_num > 10:
            raise IOError('invalid fold number')

        train_accuracy = []
        test_accuracy = []
        for i in range(args.fold_num):
            dir_path = os.path.join(args.root_dir_path, DIR_NAME.format(i))
            if not os.path.isdir(dir_path):
                continue
            log_path = os.path.join(dir_path, 'log')
            if not os.path.exists(log_path):
                raise IOError('log is not found')
            log = json.load(open(log_path))
            last_item = log[-1]
            train_accuracy.append(last_item['main/accuracy'])
            test_accuracy.append(last_item['validation/main/accuracy'])

        np_train_accuracy = np.array(train_accuracy)
        np_test_accuracy = np.array(test_accuracy)

        ave_train_accuracy = np.mean(np_train_accuracy)
        ave_test_accuracy = np.mean(np_test_accuracy)
        std_train_accuracy = np.std(np_train_accuracy)
        std_test_accuracy = np.std(np_test_accuracy)
        print('train accuracy - mean(std): {0:.5f}({1:.5f})'.format(ave_train_accuracy, std_train_accuracy))
        print('test accuracy - mean(std): {0:.5f}({1:.5f})'.format(ave_test_accuracy, std_test_accuracy))

    except IOError, e:
        print(e)
