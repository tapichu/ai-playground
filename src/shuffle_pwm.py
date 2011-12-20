#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

"""
Use a probabilistic word model to reorder a shuffled text.

This solution uses the following probabilistic model:
    * Word unigrams.
    * Naïve Bayes assumption: P(w_1, w_2... w_n) = Product(i:1..n) P(w_i).

Requirements:
    * Python 3.x
"""

import collections
import functools
import logging
import os.path
import pickle
import re
import time

# Logging level
logging.basicConfig(level=logging.DEBUG)


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


class ShuffledText:
    """Represents text split into columns."""

    def __init__(self, text=TEXT, cols=19, rows=8):
        self.original_text = text
        self.columns = []
        self.__cols = cols
        self.__rows = rows
        self.process_text(text)

        self.unigrams = WordUnigrams()

    def process_text(self, text):
        text = text.replace('\n', '')
        pieces = [piece for piece in text.split("|") if piece != '']

        for c in range(self.__cols):
            self.columns.append([])
            for r in range(self.__rows):
                self.columns[c].append(pieces[(r * self.__cols) + c])

    def column(self, n=0):
        return self.columns[n]

    def append_column(self, column):
        self.columns.append(column)

    def remove_column(self, n=0):
        column = self.columns[n]
        del self.columns[n]
        return column

    def calculate_probability(self):
        text = str(self).replace('\n', '')
        text = re.sub("[^a-z ]", "", text.lower())
        words = text.split(' ')

        probability = functools.reduce(lambda v,w: v * self.unigrams.probability(w), words, 1)
        logging.debug("Probability: %.4e", probability)
        return probability

    def __str__(self):
        string = ''
        for r in range(self.__rows):
            for c in range(self.__cols):
                string += self.columns[c][r]
            string += "\n"
        return string


class WordUnigrams:
    """Probabilistic model for word unigrams"""

    def __init__(self, word_file="count_1w.txt"):
        cwd = os.path.dirname(__file__)
        self.__words_file = os.path.join(cwd, word_file)
        self.__prob_word_model_p = os.path.join(cwd, ".prob_word_model.p")

        self.build_probabilistic_model()

    def build_probabilistic_model(self):
        """Create word unigrams, count their ocurrences and calculate their probabilities"""
        start_time = time.time()

        # TODO: fix pickle problem (can't pickle a function)
        #if os.path.isfile(self.__prob_word_model_p):
            #self.unigrams = pickle.load(open(self.__prob_word_model_p, "rb"))
        #else:
            #self.unigrams = {}
            #with open(self.__words_file, "r") as f:
                #for line in iter(f.readline, ''):
                    #parts = line.split("\t")
                    #self.unigrams[parts[0]] = {'count': int(parts[1]), 'p': 0}
                #self.calculate_probabilities()
                #pickle.dump(self.unigrams, open(self.__prob_word_model_p, "wb"))

        self.unigrams = {}
        with open(self.__words_file, "r") as f:
            for line in iter(f.readline, ''):
                parts = line.split("\t")
                self.unigrams[parts[0]] = {'count': int(parts[1]), 'p': 0}
            self.calculate_probabilities()

        logging.debug('Built probabilistic model in: %f', (time.time() - start_time))

    def calculate_probabilities(self, k=1):
        """Use Laplace smoothing to calculate the probabilities"""
        self.unigrams_count = functools.reduce(lambda v,e: v + e['count'], self.unigrams.values(), 0)
        num_unigrams = len(self.unigrams)

        for unigram in self.unigrams.values():
            unigram["p"] = (unigram["count"] + k) / (self.unigrams_count + k * num_unigrams)

        def default_p():
            return {"count": 0, "p": k / (self.unigrams_count + k * num_unigrams)}

        self.unigrams = collections.defaultdict(default_p, self.unigrams)

    def probability(self, unigram):
        """Get the probability of the specified unigram"""
        return self.unigrams[unigram]["p"]


def main():
    start_text = ShuffledText()

if __name__ == "__main__":
    main()
