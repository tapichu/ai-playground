#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "MIT License"

from .. import rotation_cipher_plm as rcplm
import unittest

class TestRotationCipher(unittest.TestCase):

    def setUp(self):
        self.rc = rcplm.RotationCipher()

    def test_alphabet(self):
        self.assertEqual(len(self.rc.alphabet), 26)

    def test_rotate_char(self):
        self.assertEqual(self.rc.rotate_char("a"), "a")
        self.assertEqual(self.rc.rotate_char("a", 1), "b")
        self.assertEqual(self.rc.rotate_char("a", 5), "f")
        self.assertEqual(self.rc.rotate_char("a", 25), "z")
        self.assertEqual(self.rc.rotate_char("a", 26), "a")

    def test_cipher(self):
        self.assertEqual(self.rc.cipher("abcd"), "abcd")
        self.assertEqual(self.rc.cipher("abcd", 1), "bcde")
        self.assertEqual(self.rc.cipher("abcd", 5), "fghi")
        self.assertEqual(self.rc.cipher("abcd", 25), "zabc")
        self.assertEqual(self.rc.cipher("abcd", 26), "abcd")

if __name__ == '__main__':
    unittest.main()
