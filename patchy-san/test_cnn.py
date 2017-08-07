#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-


import chainer
import unittest
import numpy as np
import cnn


class CnnInPatchySanTest(unittest.TestCase):

    def test_Convolution2D(self):
        """
            The conv1 convolutional layer in Patchy-san architecture is realized by means of "Convolution2D"
            offered by Chainer.
        """
        node_size = 5
        batch_size = 4
        in_channels = 2
        out_channels = 3
        rf_size = 6
        ksize = (rf_size, 1)
        initial_w = np.ones((out_channels, in_channels, ksize[0], ksize[1])).astype(np.float32)
        initial_w[:, 0, :, :] = 2 * initial_w[:, 0, :, :]
        initial_w[:, 1, :, :] = 3 * initial_w[:, 1, :, :]
        conv = chainer.links.Convolution2D(
            in_channels=in_channels,
            out_channels=out_channels,
            ksize=ksize,
            stride=ksize,
            pad=(0, 0),
            initialW=initial_w,
            initial_bias=np.ones(out_channels).astype(np.float32))

        x = np.ones((batch_size, in_channels, rf_size, node_size)).astype(np.float32)
        y = conv(x)
        self.assertTrue(np.all(y.shape == (batch_size, out_channels, 1, node_size)))
        self.assertTrue(np.all(31 == y.data))

    def test_conv1(self):
        out_channels = 3
        rf_size = 6
        ksize = (rf_size, 1)
        in_channels = 2
        initial_w = np.ones((out_channels, in_channels, ksize[0], ksize[1])).astype(np.float32)
        initial_w[:, 0, :, :] = 2 * initial_w[:, 0, :, :]
        initial_w[:, 1, :, :] = 3 * initial_w[:, 1, :, :]
        initial_bias = np.ones(out_channels).astype(np.float32)
        model = cnn.CnnInPatchySan(
            conv1_ksize=rf_size,
            conv1_output_channels=out_channels,
            conv1_initial_w=initial_w,
            conv1_initial_bias=initial_bias
        )
        batch_size = 1
        node_size = 5
        x = np.ones((batch_size, in_channels, rf_size, node_size)).astype(np.float32)
        y = model.conv1(x)
        self.assertTrue(np.all(y.shape == (batch_size, out_channels, 1, node_size)))
        self.assertTrue(np.all(31 == y.data))

    def test_conv2(self):
        out_channels = 3
        rf_size = 5
        ksize = (1, rf_size)
        in_channels = 2
        initial_w = np.ones((out_channels, in_channels, ksize[0], ksize[1])).astype(np.float32)
        initial_w[:, 0, :, :] = 2 * initial_w[:, 0, :, :]
        initial_w[:, 1, :, :] = 3 * initial_w[:, 1, :, :]
        initial_bias = np.ones((out_channels)).astype(np.float32)
        model = cnn.CnnInPatchySan(
            conv2_ksize=rf_size,
            conv2_output_channels=out_channels,
            conv2_initial_w=initial_w,
            conv2_initial_bias=initial_bias
        )
        batch_size = 1
        node_size = 100

        x = np.ones((batch_size, in_channels, 1, node_size)).astype(np.float32)
        y = model.conv2(x)
        output_node_size = (node_size - rf_size) / 1 + 1
        self.assertTrue(np.all(y.shape == (batch_size, out_channels, 1, output_node_size)))
        self.assertTrue(np.all(26 == y.data))

    def test_fc1(self):
        third_fc_output_size = 13
        model = cnn.CnnInPatchySan(fc_output_size=third_fc_output_size)
        batch_size = 1
        in_channels = 2
        node_size = 3
        x = np.ones((batch_size, in_channels, 1, node_size)).astype(np.float32)
        y = model.fc1(x)
        self.assertTrue(np.all(y.shape == (batch_size, third_fc_output_size)))

    def test_fc2(self):
        class_size = 2
        model = cnn.CnnInPatchySan(class_size=class_size)
        batch_size = 1
        node_size = 3
        x = np.ones((batch_size, node_size)).astype(np.float32)
        y = model.fc2(x)
        self.assertTrue(np.all(y.shape == (batch_size, class_size)))

    def test_call(self):
        batch_size = 13
        in_channels = 3
        rf_size = 7
        node_size = 11
        x = np.ones((batch_size, in_channels, rf_size, node_size)).astype(np.float32)

        model = cnn.CnnInPatchySan(conv1_ksize=rf_size)
        t = np.ones(batch_size).astype(np.int32)
        loss = model(x, t)
        self.assertTrue(not np.isnan(loss.data))


if __name__ == "__main__":
    unittest.main()
