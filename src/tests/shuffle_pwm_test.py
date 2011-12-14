#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

from .. import shuffle_pwm
import unittest

class TestTwoWordBigrams(unittest.TestCase):

    def setUp(self):
        self.twb = shuffle_pwm.TwoWordBigrams()

    def test_alphabet(self):
        pass

if __name__ == '__main__':
    unittest.main()
