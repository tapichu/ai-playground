#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

from .. import shuffle_pwm
import unittest
import math
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

    def test_init_with_columns(self):
        shuff = shuffle_pwm.ShuffledText(columns=[["a", "b"], ["c", "d"]], cols=2, rows=2, text=None)
        self.assertEquals(str(shuff), "ac\nbd\n")

    def test_init_with_unigrams(self):
        unigrams = shuffle_pwm.WordUnigrams()
        shuff = shuffle_pwm.ShuffledText(unigrams=unigrams)
        self.assertEquals(shuff.unigrams, unigrams)
        self.assertNotEquals(self.st.unigrams, unigrams)

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

    def test_remove_column(self):
        self.assertEquals(self.st.remove_column(4), ["a ", "  ", "ss"])
        self.assertEquals(len(self.st.columns), 4)

    def test_calculate_probability(self):
        self.assertEquals(math.exp(self.st.calculate_probability()), 2.6882067998134056e-65)


class TestWordUnigrams(unittest.TestCase):

    def setUp(self):
        self.wug = shuffle_pwm.WordUnigrams()
        self.orig_model = self.wug.model

    def test_build_probabilistic_model(self):
        self.assertEquals(len(self.wug.model), 333333)
        self.assertEquals(self.wug.model['cheese']['count'], 16704436)
        self.assertEquals(self.wug.model['shop']['count'], 212793848)

    def test_calculate_probabilities(self):
        self.wug.model = {
            "ministry": {"count": 10, "p": 0},
            "silly": {"count": 5, "p": 0},
            "walks": {"count": 0, "p": 0}
        }
        k = 2
        self.wug.calculate_probabilities(k)

        self.assertEqual(self.wug.probability("ministry"), (10 + k) / (15 + k * 3))
        self.assertEqual(self.wug.probability("silly"), (5 + k) / (15 + k * 3))
        self.assertEqual(self.wug.probability("walks"), (0 + k) / (15 + k * 3))
        self.assertEqual(self.wug.probability("none"), k / (15 + k * 3))

        # Cleanup
        self.wug.model = self.orig_model
        self.wug.calculate_probabilities()

    def test_calculate_probabilities_ml(self):
        self.wug.model = {
            "ministry": {"count": 10, "p": 0},
            "silly": {"count": 5, "p": 0},
            "walks": {"count": 0, "p": 0}
        }
        # Maximum likelihood
        self.wug.calculate_probabilities(0)

        self.assertEqual(self.wug.probability("ministry"), 10/15)
        self.assertEqual(self.wug.probability("silly"), 5/15)
        self.assertEqual(self.wug.probability("walks"), 0)
        self.assertEqual(self.wug.probability("none"), 0)

        # Cleanup
        self.wug.model = self.orig_model
        self.wug.calculate_probabilities()

    def test_probability(self):
        self.assertEqual(self.wug.probability("parrot"), 4.561720785066264e-06)

    def test_probability_not_found(self):
        self.assertEqual(self.wug.probability("paarroott"), 1.7003201005890219e-12)


class TestShufflePwm(unittest.TestCase):

    def setUp(self):
        self.text = """
|is|a |s | i|th|
|st|  |or| f|te|
|is|ss|la| c|th|
"""

    def test_most_probable(self):
        results = shuffle_pwm.most_probable(text=self.text, cols=5, rows=3)
        self.assertIsNotNone(results)
        self.assertEquals(str(results[0][1]), "this is a \ntest for  \nthis class\n")


if __name__ == '__main__':
    unittest.main()
