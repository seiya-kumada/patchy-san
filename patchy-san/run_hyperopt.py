#!/usr/bin/env python
# -*- coding: utf-8 -*-

from hyperopt import fmin, tpe, hp, STATUS_OK
import os
import subprocess


BATCH_SIZE = 'batch_size'
EPOCH_SIZE = 'epoch_size'
INPUT_DATA_DIR_PATH = '/home/ubuntu/data/patchy_san'
OUTPUT_DATA_DIR_PATH = '/home/ubuntu/results/patchy_san'

DIR_NAME = 'NCI1'
FOLDERS = ['fold_0', 'fold_1', 'fold_2', 'fold_3', 'fold_4', 'fold_5', 'fold_6', 'fold_7', 'fold_8', 'fold_9']
LABEL_OFFSET = 0


def execute_command(fold, args, output_dir_path):
    batch_size = args[BATCH_SIZE]
    epoch_size = args[EPOCH_SIZE]
    cmd = [
        './train.py',
        '--root_dir_path', os.path.join(INPUT_DATA_DIR_PATH, 'preprocessed/{}'.format(DIR_NAME)),
        '--label_path', os.path.join(INPUT_DATA_DIR_PATH, '{}.label'.format(DIR_NAME)),
        '--label_offset', str(LABEL_OFFSET),
        '--training_data_path', os.path.join(INPUT_DATA_DIR_PATH, 'preprocessed/{}/{}/train.txt'.format(DIR_NAME, fold)),
        '--testing_data_path', os.path.join(INPUT_DATA_DIR_PATH, 'preprocessed/{}/{}/test.txt'.format(DIR_NAME, fold)),
        '--out_dir_path', os.path.join(output_dir_path, fold),
        '--batch_size', str(int(batch_size)),
        '--dropout_ratio', '0.5',
        '--conv1_output_channels', '16',
        '--conv2_output_channels', '8',
        '--fc_output_size', '128',
        '--conv2_ksize', '5',
        '--test_batch_size', '10',
        '--gpu',  '0',
        '--model_epoch', '1',
        '--epoch',  str(int(epoch_size))]
    print(' '.join(cmd))
    f = subprocess.Popen(cmd)  # , stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    f.communicate()


def objective(args):
    output_dir_path = os.path.join(OUTPUT_DATA_DIR_PATH, '{}'.format(DIR_NAME))
    for fold in FOLDERS:
        execute_command(fold, args, output_dir_path)

    fold_num = len(FOLDERS)
    cmd = [
        './calculate_average_accuracy.py',
        '--root_dir_path',
        output_dir_path,
        '--fold_num',
        str(fold_num)]
    f = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    stdout, _ = f.communicate()
    lines = stdout.split('\n')
    tokens = lines[1].split()
    loss = None
    try:
        loss = tokens[-1].split('(')[0]
    except IndexError, e:
        print(e)
        print(tokens)
        raise IndexError("")

    return {'loss': -float(loss), 'status': STATUS_OK}


if __name__ == '__main__':
    pass
    best = fmin(
        fn=objective,
        space={
            BATCH_SIZE: hp.quniform(BATCH_SIZE, 10, 100, 10),
            EPOCH_SIZE: hp.quniform(EPOCH_SIZE, 10, 50, 10),
        },
        algo=tpe.suggest,
        max_evals=1)

    print(best)
