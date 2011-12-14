#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

"""
Use a probabilistic word model to reorder a shuffled text.

This solution uses the following probabilistic model:
    * 2 word bigrams.
    * Markov assumption: P(w_1, w_2... w_n) = Product(i:1..n) P(w_i|w_i-1).

Requirements:
    * Python 3.x
"""

import logging
import os.path

# Logging level
logging.basicConfig(level=logging.INFO)


# The text we want to reorder
TEXT = """
|de|  | f|Cl|nf|ed|au| i|ti|  |ma|ha|or|nn|ou| S|on|nd|on|
|ry|  |is|th|is| b|eo|as|  |  |f |wh| o|ic| t|, |  |he|h |
|ab|  |la|pr|od|ge|ob| m|an|  |s |is|el|ti|ng|il|d |ua|c |
|he|  |ea|of|ho| m| t|et|ha|  | t|od|ds|e |ki| c|t |ng|br|
|wo|m,|to|yo|hi|ve|u | t|ob|  |pr|d |s |us| s|ul|le|ol|e |
| t|ca| t|wi| M|d |th|"A|ma|l |he| p|at|ap|it|he|ti|le|er|
|ry|d |un|Th|" |io|eo|n,|is|  |bl|f |pu|Co|ic| o|he|at|mm|
|hi|  |  |in|  |  | t|  |  |  |  |ye|  |ar|  |s |  |  |. |
"""


class TwoWordBigrams:
    """Probabilistic word model for 2 word bigrams"""

    def __init__(self):
        cwd = os.path.dirname(__file__)
        self.__words_file = os.path.join(cwd, "count_2w.txt")
        self.__word_counts_p = os.path.join(cwd, ".word_counts.p")
        self.__prob_word_model_p = os.path.join(cwd, ".prob_word_model.p")

    def build_probabilistic_model(self):
        pass

    def calculate_probabilities(self, k=2):
        pass

    def probability(self, bigram):
        pass


def main():
    print(TEXT)

if __name__ == "__main__":
    main()
