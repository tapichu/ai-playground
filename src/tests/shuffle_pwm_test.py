#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

from .. import shuffle_pwm
import unittest
import os.path

cwd = os.path.dirname(__file__)

TEST_TEXT = """
th|is| i|s |a |
te|st| f|or|  |
th|is| c|la|ss|
"""

class TestSuffledText(unittest.TestCase):

    def setUp(self):
        self.st = shuffle_pwm.ShuffledText(text=TEST_TEXT, cols=5, rows=3)

    def test_process_text(self):
        self.assertEquals(self.st.columns[0], ["th", "te", "th"])
        self.assertEquals(self.st.columns[4], ["a ", "  ", "ss"])

    def test_str(self):
        text = str(self.st)
        self.assertEquals(text, "this is a \ntest for  \nthis class\n")

    def test_column(self):
        self.assertEquals(self.st.column(0), ["th", "te", "th"])
        self.assertEquals(self.st.column(4), ["a ", "  ", "ss"])

    def test_append_column(self):
        column = ["  ", "  ", "s."]
        self.st.append_column(column)
        self.assertEquals(self.st.column(5), column)


class TestWordUnigrams(unittest.TestCase):

    def setUp(self):
        self.wug = shuffle_pwm.WordUnigrams()

    def test_build_probabilistic_model(self):
        self.assertEquals(len(self.wug.unigrams), 333333)
        self.assertEquals(self.wug.unigrams['cheese']['count'], 16704436)
        self.assertEquals(self.wug.unigrams['shop']['count'], 212793848)

    def test_calculate_probabilities(self):
        self.wug.unigrams = {
            "ministry": {"count": 10, "p": 0},
            "silly": {"count": 5, "p": 0},
            "walks": {"count": 0, "p": 0}
        }
        k = 2
        self.wug.calculate_probabilities(k)

        self.assertEqual(self.wug.probability("ministry"), (10 + k) / (15 + k * 3))
        self.assertEqual(self.wug.probability("silly"), (5 + k) / (15 + k * 3))
        self.assertEqual(self.wug.probability("walks"), (0 + k) / (15 + k * 3))

    def test_calculate_probabilities_ml(self):
        self.wug.unigrams = {
            "ministry": {"count": 10, "p": 0},
            "silly": {"count": 5, "p": 0},
            "walks": {"count": 0, "p": 0}
        }
        # Maximum likelihood
        self.wug.calculate_probabilities(0)

        self.assertEqual(self.wug.probability("ministry"), 10/15)
        self.assertEqual(self.wug.probability("silly"), 5/15)
        self.assertEqual(self.wug.probability("walks"), 0)

    def test_probability(self):
        self.assertEqual(self.wug.probability("parrot"), 4.561720785066264e-06)

if __name__ == '__main__':
    unittest.main()
