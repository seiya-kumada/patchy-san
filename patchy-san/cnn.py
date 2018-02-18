#!/usr/bin/env python
# -*- coding: utf-8 -*-


import chainer
import chainer.functions as F
import chainer.links as L


class CnnInPatchySan(chainer.Chain):

    def __init__(
        self,
        conv1_ksize=10,
        conv1_output_channels=16,
        conv1_initial_w=None,
        conv1_initial_bias=None,
        conv2_ksize=10,
        conv2_output_channels=8,
        conv2_initial_w=None,
        conv2_initial_bias=None,
        fc_output_size=128,
        class_size=2,
        dropout_ratio=0.5
    ):

        fksize = (conv1_ksize, 1)
        sksize = (1, conv2_ksize)
        sstride = (1, 1)

        super(CnnInPatchySan, self).__init__(
            conv1=L.Convolution2D(
                in_channels=None,  # automatically determined
                out_channels=conv1_output_channels,
                ksize=fksize,
                stride=fksize,
                pad=(0, 0),
                initialW=conv1_initial_w,
                initial_bias=conv1_initial_bias),

            conv2=L.Convolution2D(
                in_channels=None,  # automatically determined
                out_channels=conv2_output_channels,
                ksize=sksize,
                stride=sstride,
                pad=(0, 0),
                initialW=conv2_initial_w,
                initial_bias=conv2_initial_bias),

            fc1=L.Linear(in_size=None, out_size=fc_output_size, initialW=conv2_initial_w, initial_bias=conv2_initial_bias),
            fc2=L.Linear(in_size=None, out_size=class_size, initialW=conv2_initial_w, initial_bias=conv2_initial_bias),
            n1=L.BatchNormalization(conv1_output_channels),
            n2=L.BatchNormalization(conv2_output_channels),
            n3=L.BatchNormalization(conv2_output_channels),
            n4=L.BatchNormalization(fc_output_size)
        )
        self.select_phase('train')
        self.dropout_ratio = dropout_ratio

    def select_phase(self, phase):
        if phase == 'predict':
            self.train = False
            self.predict = True
        elif phase == 'train':
            self.train = True
            self.predict = False
        elif phase == 'test':
            self.train = False
            self.predict = False
        else:
            raise Exception('unknown phase')

    def __call__(self, x, t):
        h = self.conv1(x)
        h = self.n1(h)
        h = F.relu(h)
        h = F.dropout(h, ratio=self.dropout_ratio, train=self.train)

        h = self.conv2(h)
        h = self.n2(h)
        h = F.relu(h)
        h = F.dropout(h, ratio=self.dropout_ratio, train=self.train)

        h = self.n3(h)
        h = F.relu(h)
        h = self.fc1(h)

        h = self.n4(h)
        h = F.relu(h)
        h = self.fc2(h)

        if self.predict:
            return F.softmax(h)
        else:
            loss = F.softmax_cross_entropy(h, t)
            accuracy = F.accuracy(h, t)
            chainer.report({'loss': loss, 'accuracy': accuracy}, self)
            return loss
