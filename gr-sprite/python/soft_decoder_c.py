#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 
# Copyright 2015 Zac Manchester.
# 
# This is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3, or (at your option)
# any later version.
# 
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this software; see the file COPYING.  If not, write to
# the Free Software Foundation, Inc., 51 Franklin Street,
# Boston, MA 02110-1301, USA.
# 

from __future__ import print_function
from math import *
from numpy import *
from gnuradio import gr

class soft_decoder_c(gr.sync_block):
    """
    docstring for block soft_decoder_c
    """
    def __init__(self):
        gr.sync_block.__init__(self, name="soft_decoder_c", in_sig=[complex64], out_sig=[])

        self.set_history(30)
        self._detection_threshold = .85
    
        self._preamble = array([1, 1, 1, -1, -1, 1, -1], dtype=float32)
        self._postamble = array([1, -1, 1, 1, -1, -1, -1], dtype=float32)
        self._template = hstack([self._preamble, zeros(16, dtype=float32), self._postamble])/sqrt(14)

        self._C = array([
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],
            [1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, 1],
            [-1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 1, -1],
            [1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, 1],
            [1, 1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1],
            [-1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, 1],
            [1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, -1, 1, 1, -1],
            [-1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, 1, 1],
            [-1, -1, 1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1],
            [1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1],
            [-1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1],
            [1, -1, -1, 1, 1, 1, -1, -1, -1, -1, -1, -1, 1, -1, 1, 1],
            [1, 1, -1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1],
            [-1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, 1],
            [1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1],
            [-1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, -1, 1, 1, 1, 1],
            [-1, 1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, -1],
            [1, -1, 1, 1, -1, -1, -1, -1, -1, -1, -1, 1, -1, -1, -1, 1],
            [-1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1],
            [1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1],
            [1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, -1],
            [-1, 1, -1, -1, -1, -1, 1, -1, -1, -1, -1, 1, -1, 1, -1, 1],
            [1, 1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1],
            [-1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, 1],
            [-1, 1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1],
            [1, -1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, 1],
            [-1, -1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1],
            [1, 1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, 1],
            [1, -1, 1, -1, -1, 1, 1, -1, -1, -1, -1, 1, 1, 1, -1, -1],
            [-1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, 1],
            [1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1],
            [-1, -1, -1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, 1],
            [1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, -1],
            [-1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1],
            [1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, -1],
            [-1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1],
            [-1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, -1],
            [1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1],
            [-1, 1, -1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, 1, -1],
            [1, -1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, -1, -1, -1, 1, -1, 1, -1, -1, -1],
            [-1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, 1],
            [1, -1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1],
            [-1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1],
            [-1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1, 1, 1, -1, -1],
            [1, 1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, 1],
            [-1, 1, 1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, 1, -1],
            [1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, 1],
            [1, -1, 1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1],
            [-1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1, 1],
            [1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1, 1, -1, -1, 1, -1],
            [-1, -1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1],
            [-1, 1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1],
            [1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, -1, 1],
            [-1, -1, 1, -1, -1, -1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1],
            [1, 1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1],
            [1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1, -1],
            [-1, 1, -1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, 1],
            [1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1],
            [-1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1],
            [-1, 1, 1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, -1, -1],
            [1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1],
            [-1, -1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1],
            [1, 1, -1, -1, -1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1],
            [-1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, -1, -1, -1, -1, -1],
            [1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, -1, 1],
            [-1, -1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1],
            [1, 1, 1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1, 1],
            [1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1],
            [-1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1],
            [1, 1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, -1],
            [-1, -1, -1, 1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1, 1, 1],
            [-1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1],
            [1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1],
            [-1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1],
            [1, 1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1],
            [1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1],
            [-1, 1, -1, 1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1],
            [1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1],
            [-1, -1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1],
            [-1, -1, 1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1, -1],
            [1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1],
            [-1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, -1],
            [1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1],
            [1, 1, -1, 1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, -1],
            [-1, -1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1],
            [1, -1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1],
            [-1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, 1, 1],
            [-1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1],
            [1, 1, -1, -1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, 1],
            [-1, 1, 1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1],
            [1, -1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1],
            [1, 1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1],
            [-1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, -1, 1],
            [1, -1, -1, 1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1],
            [-1, 1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1],
            [1, -1, -1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1, -1, -1],
            [-1, 1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1],
            [1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, -1],
            [-1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, -1, 1, 1],
            [-1, 1, 1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1, -1],
            [1, -1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1],
            [-1, -1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1],
            [1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, 1, 1],
            [1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1],
            [-1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, -1, -1, 1],
            [1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1, 1, -1, 1, -1],
            [-1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1],
            [-1, 1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1],
            [1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, 1, -1, 1],
            [-1, -1, 1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1],
            [1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1],
            [1, 1, 1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, -1, -1, -1],
            [-1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, 1],
            [1, -1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, 1, -1],
            [-1, 1, -1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1],
            [-1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1],
            [1, 1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1],
            [-1, 1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1],
            [1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1],
            [1, 1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1],
            [-1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1],
            [1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1],
            [-1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1],
            [-1, -1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1],
            [1, 1, 1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1],
            [-1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1],
            [1, -1, -1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1],
            [1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1, -1, -1],
            [-1, 1, -1, -1, 1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1, 1],
            [1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, -1, -1, -1, 1, -1],
            [-1, -1, 1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, 1, 1],
            [-1, 1, 1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1, 1, -1, -1],
            [1, -1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1, -1, 1],
            [-1, -1, -1, 1, -1, 1, -1, -1, 1, -1, -1, -1, -1, 1, 1, -1],
            [1, 1, -1, -1, -1, -1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1],
            [1, -1, 1, -1, 1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1, -1],
            [-1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, -1, 1, -1, -1, 1],
            [1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1],
            [-1, -1, -1, -1, -1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1],
            [-1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1, 1, 1, -1, -1],
            [1, -1, -1, -1, 1, -1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1],
            [-1, -1, 1, -1, -1, 1, 1, 1, 1, -1, -1, -1, 1, 1, 1, -1],
            [1, 1, 1, 1, -1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, -1, -1],
            [-1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, 1, -1, -1, -1, 1],
            [1, -1, -1, -1, -1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1, -1],
            [-1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1, 1, 1],
            [-1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1],
            [1, 1, -1, 1, 1, 1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1],
            [-1, 1, 1, 1, -1, -1, 1, 1, 1, -1, -1, 1, -1, 1, 1, -1],
            [1, -1, 1, -1, -1, 1, -1, -1, 1, -1, -1, 1, -1, 1, 1, 1],
            [1, 1, -1, -1, 1, -1, 1, -1, 1, -1, -1, 1, 1, -1, -1, -1],
            [-1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1],
            [1, -1, 1, 1, -1, -1, 1, -1, 1, -1, -1, 1, 1, -1, 1, -1],
            [-1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, 1],
            [-1, -1, 1, 1, 1, -1, -1, -1, 1, -1, -1, 1, 1, 1, -1, -1],
            [1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1],
            [-1, 1, -1, -1, -1, -1, -1, -1, 1, -1, -1, 1, 1, 1, 1, -1],
            [1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1],
            [-1, 1, -1, 1, -1, -1, 1, 1, 1, -1, 1, -1, -1, -1, -1, -1],
            [1, -1, -1, -1, -1, 1, -1, -1, 1, -1, 1, -1, -1, -1, -1, 1],
            [-1, -1, 1, -1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1, 1, -1],
            [1, 1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1, -1, -1, 1, 1],
            [1, -1, 1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, 1, -1, -1],
            [-1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, -1, -1, 1, -1, 1],
            [1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1],
            [-1, -1, -1, -1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1, 1, 1],
            [-1, 1, 1, -1, -1, -1, -1, -1, 1, -1, 1, -1, 1, -1, -1, -1],
            [1, -1, 1, 1, -1, 1, 1, 1, 1, -1, 1, -1, 1, -1, -1, 1],
            [-1, -1, -1, 1, 1, -1, -1, -1, 1, -1, 1, -1, 1, -1, 1, -1],
            [1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, -1, 1, 1],
            [1, -1, -1, 1, -1, -1, 1, -1, 1, -1, 1, -1, 1, 1, -1, -1],
            [-1, 1, -1, -1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1],
            [1, 1, 1, -1, 1, -1, 1, -1, 1, -1, 1, -1, 1, 1, 1, -1],
            [-1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1, 1],
            [-1, -1, 1, 1, -1, 1, -1, -1, 1, -1, 1, 1, -1, -1, -1, -1],
            [1, 1, 1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1, -1, 1],
            [-1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1, -1, -1, 1, -1],
            [1, -1, -1, 1, 1, -1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1],
            [1, 1, -1, -1, -1, 1, 1, -1, 1, -1, 1, 1, -1, 1, -1, -1],
            [-1, -1, -1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1, 1],
            [1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, -1],
            [-1, 1, 1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1],
            [-1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, -1, -1],
            [1, 1, -1, 1, -1, -1, -1, -1, 1, -1, 1, 1, 1, -1, -1, 1],
            [-1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1],
            [1, -1, 1, -1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, 1],
            [1, 1, 1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1],
            [-1, -1, 1, -1, -1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1],
            [1, -1, -1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1],
            [-1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 1, 1],
            [1, 1, -1, 1, -1, -1, -1, -1, 1, 1, -1, -1, -1, -1, -1, -1],
            [-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1, -1, -1, -1, -1, 1],
            [1, -1, 1, -1, 1, -1, -1, -1, 1, 1, -1, -1, -1, -1, 1, -1],
            [-1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1],
            [-1, -1, 1, -1, -1, -1, 1, -1, 1, 1, -1, -1, -1, 1, -1, -1],
            [1, 1, 1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, -1, 1],
            [-1, 1, -1, 1, 1, -1, 1, -1, 1, 1, -1, -1, -1, 1, 1, -1],
            [1, -1, -1, -1, 1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1],
            [1, 1, 1, -1, -1, -1, 1, 1, 1, 1, -1, -1, 1, -1, -1, -1],
            [-1, -1, 1, 1, -1, 1, -1, -1, 1, 1, -1, -1, 1, -1, -1, 1],
            [1, -1, -1, 1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1, 1, -1],
            [-1, 1, -1, -1, 1, 1, -1, -1, 1, 1, -1, -1, 1, -1, 1, 1],
            [-1, -1, -1, 1, -1, -1, -1, 1, 1, 1, -1, -1, 1, 1, -1, -1],
            [1, 1, -1, -1, -1, 1, 1, -1, 1, 1, -1, -1, 1, 1, -1, 1],
            [-1, 1, 1, -1, 1, -1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1],
            [1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1],
            [1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, -1, -1, -1, -1],
            [-1, 1, 1, -1, -1, -1, -1, -1, 1, 1, -1, 1, -1, -1, -1, 1],
            [1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1, -1, 1, -1],
            [-1, -1, -1, 1, 1, -1, -1, -1, 1, 1, -1, 1, -1, -1, 1, 1],
            [-1, 1, -1, -1, -1, 1, -1, 1, 1, 1, -1, 1, -1, 1, -1, -1],
            [1, -1, -1, 1, -1, -1, 1, -1, 1, 1, -1, 1, -1, 1, -1, 1],
            [-1, -1, 1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, 1, -1],
            [1, 1, 1, -1, 1, -1, 1, -1, 1, 1, -1, 1, -1, 1, 1, 1],
            [1, -1, -1, -1, -1, 1, -1, -1, 1, 1, -1, 1, 1, -1, -1, -1],
            [-1, 1, -1, 1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1, -1, 1],
            [1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1, 1, 1, -1, 1, -1],
            [-1, -1, 1, -1, 1, -1, 1, 1, 1, 1, -1, 1, 1, -1, 1, 1],
            [-1, 1, 1, 1, -1, 1, 1, -1, 1, 1, -1, 1, 1, 1, -1, -1],
            [1, -1, 1, -1, -1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1],
            [-1, -1, -1, -1, 1, 1, 1, -1, 1, 1, -1, 1, 1, 1, 1, -1],
            [1, 1, -1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1],
            [-1, -1, -1, 1, 1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1, -1],
            [1, 1, -1, -1, 1, -1, 1, -1, 1, 1, 1, -1, -1, -1, -1, 1],
            [-1, 1, 1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, 1, -1],
            [1, -1, 1, 1, -1, -1, 1, -1, 1, 1, 1, -1, -1, -1, 1, 1],
            [1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, -1, -1, 1, -1, -1],
            [-1, -1, 1, 1, 1, -1, -1, -1, 1, 1, 1, -1, -1, 1, -1, 1],
            [1, -1, -1, 1, -1, 1, 1, 1, 1, 1, 1, -1, -1, 1, 1, -1],
            [-1, 1, -1, -1, -1, -1, -1, -1, 1, 1, 1, -1, -1, 1, 1, 1],
            [-1, -1, 1, -1, 1, 1, 1, -1, 1, 1, 1, -1, 1, -1, -1, -1],
            [1, 1, 1, 1, 1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1, 1],
            [-1, 1, -1, 1, -1, 1, 1, -1, 1, 1, 1, -1, 1, -1, 1, -1],
            [1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, 1, 1],
            [1, 1, -1, 1, 1, 1, -1, -1, 1, 1, 1, -1, 1, 1, -1, -1],
            [-1, -1, -1, -1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1, -1, 1],
            [1, -1, 1, -1, -1, 1, -1, -1, 1, 1, 1, -1, 1, 1, 1, -1],
            [-1, 1, 1, 1, -1, -1, 1, 1, 1, 1, 1, -1, 1, 1, 1, 1],
            [-1, 1, 1, 1, 1, -1, 1, -1, 1, 1, 1, 1, -1, -1, -1, -1],
            [1, -1, 1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, -1, 1],
            [-1, -1, -1, -1, -1, -1, 1, -1, 1, 1, 1, 1, -1, -1, 1, -1],
            [1, 1, -1, 1, -1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1, 1],
            [1, -1, -1, -1, 1, -1, -1, -1, 1, 1, 1, 1, -1, 1, -1, -1],
            [-1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1, 1, -1, 1],
            [1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, 1, 1, -1],
            [-1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, -1, 1, 1, 1],
            [-1, 1, -1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1, -1, -1],
            [1, -1, -1, 1, 1, 1, 1, -1, 1, 1, 1, 1, 1, -1, -1, 1],
            [-1, -1, 1, 1, -1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1, -1],
            [1, 1, 1, -1, -1, 1, 1, -1, 1, 1, 1, 1, 1, -1, 1, 1],
            [1, -1, 1, 1, 1, -1, 1, 1, 1, 1, 1, 1, 1, 1, -1, -1],
            [-1, 1, 1, -1, 1, 1, -1, -1, 1, 1, 1, 1, 1, 1, -1, 1],
            [1, 1, -1, -1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1, 1, -1],
            [-1, -1, -1, 1, -1, 1, -1, -1, 1, 1, 1, 1, 1, 1, 1, 1]
            ], dtype=float32)/sqrt(16)

    def work(self, input_items, output_items):
        in0 = input_items[0]

        k = 0
        max_index = len(in0)-29
        while k < max_index:
            
            cor1 = dot(real(in0[k:k+30]), self._template)/sqrt(dot(real(in0[k:k+7]),real(in0[k:k+7]))+dot(real(in0[k+23:k+30]),real(in0[k+23:k+30])))
            cor2 = dot(imag(in0[k:k+30]), self._template)/sqrt(dot(imag(in0[k:k+7]),imag(in0[k:k+7]))+dot(imag(in0[k+23:k+30]),imag(in0[k+23:k+30])))
            
            if cor1 > self._detection_threshold:
                codeword = real(in0[k+7:k+23])
                cor3 = dot(self._C,codeword)/sqrt(dot(codeword,codeword))
                k += 30
                if max(cor3) > self._detection_threshold:
                    print(chr(argmax(cor3)), end='')
                    
            elif cor2 > self._detection_threshold:
                codeword = imag(in0[k+7:k+23])
                cor3 = dot(self._C,codeword)/sqrt(dot(codeword,codeword))
                k += 30
                if max(cor3) > self._detection_threshold:
                    print(chr(argmax(cor3)), end='')
            else:
                k += 1

        if max_index < 1:
            return 0
        elif k > max_index:
            return k
        else:
            return max_index
