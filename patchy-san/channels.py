#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import numpy as np


class ChannelsBase(object):

    def __init__(self, num_channels):
        self.num_channels = num_channels

    def set_graph(self, graph):
        self.graph = graph

    def __call__(self, v):
        return np.empty(self.num_channels).astype(np.float32)
