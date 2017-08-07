#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from channels import *  # noqa


class Channels(ChannelsBase):

    # test ok
    def __call__(self, v):
        return self.graph.vp.label[v]
