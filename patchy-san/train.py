#!/usr/bin/env python2.7
# coding:utf-8

import numpy as np
from chainer import initializers
import chainer
import cnn
from chainer.training import extensions
import os
import argparse
from chainer import training
import dataset


def check_path(path):
    if not os.path.exists(path):
        raise IOError("{} is not found".format(path))


def load_labels(path):
    items = open(path).readlines()[0].split()
    s = set(items)
    return len(s)


class TestModeEvaluator(extensions.Evaluator):

    def evaluate(self):
        model = self.get_target('main')
        model.select_phase('test')
        ret = super(TestModeEvaluator, self).evaluate()
        model.select_phase('train')
        return ret


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser()
        parser.add_argument("--root_dir_path", help="input: set a path to an training/testing directory")
        parser.add_argument("--label_path", help="input: set a path to a label file")
        parser.add_argument("--label_offset", type=np.int32, default=0,
                            help="input: offset number for labels. Label is set to 'label' - 'offset'.")
        parser.add_argument("--training_data_path", help="input: set a path to a training data file(.txt)")
        parser.add_argument("--testing_data_path", help="input: set a path to a testing data file(.txt)")
        parser.add_argument("--gpu", type=int, default=-1, help="input: GPU ID(negative value indicates CPU")
        parser.add_argument('--loader_job', type=int, default=2,
                            help='input: number of parallel data loading processes')
        parser.add_argument('--batch_size', type=int, default=32, help='input: learning minibatch size')
        parser.add_argument('--test_batch_size', type=int, default=250, help='input: testing minibatch size')
        parser.add_argument('--epoch', type=int, default=10, help='input: number of epochs to train')
        parser.add_argument('--out_dir_path', default='result', help='output: set a path to output directory')
        parser.add_argument('--test', action='store_true', default=False,
                            help='option: test mode if this flag is set(default: False)')
        parser.add_argument('--resume', default='', help='option: initialize the trainer from given file')
        parser.add_argument('--model_epoch', type=int, default=1, help='input: epoch to save model')
        parser.add_argument('--dropout_ratio', type=float, default=0.5, help='input: dropout ratio')
        parser.add_argument('--conv1_output_channels', type=int, default=16,
                            help='input: number of the first conv output channels')
        parser.add_argument('--conv2_output_channels', type=int, default=8,
                            help='input: number of the second conv output channels')
        parser.add_argument('--fc_output_size', type=int, default=128,
                            help='input: unit number of the full connected layer')
        parser.add_argument('--conv2_ksize', type=int, default=3,
                            help='input: size of receptive field in the second conv layer')
        args = parser.parse_args()

        # get paths
        root_dir_path = args.root_dir_path
        label_path = args.label_path
        training_data_path = args.training_data_path
        testing_data_path = args.testing_data_path
        out_dir_path = args.out_dir_path

        # check paths
        check_path(root_dir_path)
        check_path(label_path)
        check_path(training_data_path)
        check_path(testing_data_path)
        check_path(out_dir_path)

        print("# _/_/_/ load model _/_/_/")
        class_size = load_labels(label_path)
        print('class_size: {}'.format(class_size))

        # load a model
        W = initializers.HeNormal(1 / np.sqrt(2), np.float32)
        bias = initializers.Zero(np.float32)
        model = cnn.CnnInPatchySan(
            conv1_ksize=10,  # depend on an input shape
            conv1_output_channels=args.conv1_output_channels,
            conv1_initial_w=W,
            conv1_initial_bias=bias,
            conv2_ksize=args.conv2_ksize,
            conv2_output_channels=args.conv2_output_channels,
            conv2_initial_w=W,
            conv2_initial_bias=bias,
            fc_output_size=args.fc_output_size,
            class_size=class_size,
            dropout_ratio=args.dropout_ratio,
        )

        if args.gpu >= 0:
            chainer.cuda.get_device(args.gpu).use()  # make the GPU current
            model.to_gpu()

        print("# _/_/_/ load dataset _/_/_/")

        train = dataset.Dataset(training_data_path, root_dir_path, args.label_offset)
        test = dataset.Dataset(testing_data_path, root_dir_path, args.label_offset)

        train_iter = chainer.iterators.MultiprocessIterator(train, args.batch_size, n_processes=args.loader_job, shuffle=True)
        test_iter = chainer.iterators.MultiprocessIterator(test, args.test_batch_size, repeat=False,
                                                           n_processes=args.loader_job)

        log_interval = int(len(train) / float(args.batch_size))

        print("# _/_/_/ set up an optimizer _/_/_/")

        # optimizer = chainer.optimizers.MomentumSGD(lr=0.0001, momentum=0.97)
        # optimizer = chainer.optimizers.Adam()
        optimizer = chainer.optimizers.RMSprop(lr=0.001)
        optimizer.setup(model)

        print("# _/_/_/ set up a trainer _/_/_/")

        updater = training.StandardUpdater(train_iter, optimizer, device=args.gpu)
        trainer = training.Trainer(updater, (args.epoch, 'epoch'), args.out_dir_path)

        log_interval = (10 if args.test else log_interval), 'iteration'
        model_epoch = (1 if args.test else args.model_epoch), 'epoch'

        trainer.extend(TestModeEvaluator(test_iter, model, device=args.gpu), trigger=log_interval)
        trainer.extend(extensions.ExponentialShift('lr', 0.99), trigger=model_epoch)

        # Save two plot images to the result dir
        trainer.extend(
            extensions.PlotReport(['main/loss', 'validation/main/loss'],
                                  'epoch', file_name='loss.png'))
        trainer.extend(
            extensions.PlotReport(
                ['main/accuracy', 'validation/main/accuracy'],
                'epoch', file_name='accuracy.png'))

        # trainer.extend(extensions.dump_graph('main/loss'))  # yield cg.dot
        # trainer.extend(extensions.snapshot(), trigger=model_epoch)  # save a trainer for resuming training
        # trainer.extend(extensions.snapshot_object(model, 'model_iter_{.updater.iteration}',
        #                                           trigger=model_epoch))  # save a modified model

        # Be careful to pass the interval directly to LogReport
        # (it determines when to emit log rather than when to read observations)
        trainer.extend(extensions.LogReport(trigger=log_interval))
        trainer.extend(extensions.observe_lr(), trigger=log_interval)
        trainer.extend(
            extensions.PrintReport(
                ['epoch', 'iteration', 'main/loss', 'validation/main/loss', 'main/accuracy',
                 'validation/main/accuracy', 'lr']
            ),
            trigger=log_interval)
        trainer.extend(extensions.ProgressBar(update_interval=10))

        if args.resume:
            chainer.serializers.load_npz(args.resume, trainer)

        trainer.run()
    except IOError, e:
        print(e)
