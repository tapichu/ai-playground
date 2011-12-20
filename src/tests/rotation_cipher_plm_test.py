#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

from .. import rotation_cipher_plm as rcplm
import unittest
import functools

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

    def test_encode(self):
        self.assertEqual(self.rc.encode("abcd"), "abcd")
        self.assertEqual(self.rc.encode("abcd", 1), "bcde")
        self.assertEqual(self.rc.encode("abcd", 5), "fghi")
        self.assertEqual(self.rc.encode("abcd", 25), "zabc")
        self.assertEqual(self.rc.encode("abcd", 26), "abcd")

    def test_encode_special_chars(self):
        self.assertEqual(self.rc.encode("ab cd", 1), "bc de")
        self.assertEqual(self.rc.encode("ab cd!", 1), "bc de!")


class TestLetterBigrams(unittest.TestCase):

    def setUp(self):
        self.lbg = rcplm.LetterBigrams()

    def test_init(self):
        self.assertEqual(len(self.lbg.words), 267751)

    def test_init_lowercase(self):
        self.assertEqual(self.lbg.words[0], "aa")

    def test_build_probabilistic_model(self):
        self.assertEqual(self.lbg.bigrams['aa'], {"count": 194, "p": 8.977135925347058e-05})
        self.assertEqual(self.lbg.bigrams['za'], {"count": 1729, "p": 0.0007964330846589955})
        bigrams_count = functools.reduce(lambda v,e: v + e['count'], self.lbg.bigrams.values(), 0)
        self.assertEqual(bigrams_count, 2171509)

    def test_calculate_probabilities(self):
        self.lbg.bigrams = {
            "aa": {"count": 10, "p": 0},
            "ab": {"count": 5, "p": 0},
            "ac": {"count": 0, "p": 0}
        }
        k = 2
        self.lbg.calculate_probabilities(k)

        self.assertEqual(self.lbg.probability("aa"), (10 + k) / (15 + k * 3))
        self.assertEqual(self.lbg.probability("ab"), (5 + k) / (15 + k * 3))
        self.assertEqual(self.lbg.probability("ac"), (0 + k) / (15 + k * 3))

    def test_calculate_probabilities_ml(self):
        self.lbg.bigrams = {
            "aa": {"count": 10, "p": 0},
            "ab": {"count": 5, "p": 0},
            "ac": {"count": 0, "p": 0}
        }
        # Maximum likelihood
        self.lbg.calculate_probabilities(0)

        self.assertEqual(self.lbg.probability("aa"), 10/15)
        self.assertEqual(self.lbg.probability("ab"), 5/15)
        self.assertEqual(self.lbg.probability("ac"), 0)

    def test_probability(self):
        self.assertEqual(self.lbg.probability("za"), 0.0007964330846589955)


class TestDecoder(unittest.TestCase):

    def setUp(self):
        rotation_cipher = rcplm.RotationCipher()
        self.phrase = "Tonight instead of discussing the existence or non existence \
of God they have decided to fight for it"
        encoded_phrase = rotation_cipher.encode(self.phrase, 5)
        self.phrases = [rotation_cipher.encode(encoded_phrase, x) for x in range(0, 26)]

    def test_most_probable(self):
        sorted_phrases = rcplm.most_probable(self.phrases)
        self.assertEqual(len(sorted_phrases), 26)
        self.assertEqual(sorted_phrases[0][1], self.phrase.lower())
        self.assertEqual(sorted_phrases[0][0], 2.3102527364450072e-156)
        self.assertEqual(sorted_phrases[1][0], 2.7518911947067603e-214)

if __name__ == '__main__':
    unittest.main()
