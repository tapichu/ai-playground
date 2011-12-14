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
        self.assertEqual(self.rc.cipher("ab cd", 1), "bc de")

class TestLetterBigrams(unittest.TestCase):

    @classmethod
    def setUpClass(klass):
        klass.lng = rcplm.LetterBigrams()

    def test_init(self):
        self.assertEqual(len(self.lng.words), 267751)

    def test_init_lowercase(self):
        self.assertEqual(self.lng.words[0], "aa")

    def test_build_probabilistic_model(self):
        self.assertEqual(self.lng.bigrams['aa'], {"count": 194, "p": 9.025973158782064e-05})
        self.assertEqual(self.lng.bigrams['za'], {"count": 1729, "p": 0.0007971407927475385})
        self.assertEqual(self.lng.bigrams_count, 2171509)

    def test_probability(self):
        self.assertEqual(self.lng.probability("za"), 0.0007971407927475385)

if __name__ == '__main__':
    unittest.main()
