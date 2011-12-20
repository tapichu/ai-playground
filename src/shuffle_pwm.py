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

import functools
import logging
import os.path
import math
import pickle
import re
import time

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


class ShuffledText:
    """Represents text split into columns."""

    def __init__(self, text=TEXT, cols=19, rows=8, columns=None, unigrams=None):
        self.__cols = cols
        self.__rows = rows
        self.columns = columns if columns else []
        self.unigrams = unigrams if unigrams else WordUnigrams()

        if text:
            self.original_text = text
            self.process_text(text)

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
        self.__cols += 1

    def remove_column(self, n=0):
        column = self.columns[n]
        del self.columns[n]
        self.__cols -= 1
        return column

    def calculate_probability(self):
        text = str(self).replace('\n', ' ')
        text = re.sub("[^a-z ]", "", text.lower())
        words = text.split(' ')

        # Use logs, the probabilities are quite small
        probability = functools.reduce(
                lambda v,w: v + math.log(self.unigrams.probability(w)), words, 0)
        logging.debug("Probability: %f", probability)
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
        self.__default_prob_p = os.path.join(cwd, ".default_prob.p")

        self.build_probabilistic_model()

    def build_probabilistic_model(self):
        """Create word unigrams, count their ocurrences and calculate their probabilities"""
        start_time = time.time()

        if os.path.isfile(self.__prob_word_model_p):
            self.unigrams = pickle.load(open(self.__prob_word_model_p, "rb"))
        else:
            self.unigrams = {}
            with open(self.__words_file, "r") as f:
                for line in iter(f.readline, ''):
                    parts = line.split("\t")
                    self.unigrams[parts[0]] = {'count': int(parts[1]), 'p': 0}
                self.calculate_probabilities()
                pickle.dump(self.unigrams, open(self.__prob_word_model_p, "wb"))

        if os.path.isfile(self.__default_prob_p):
            self.default_prob = pickle.load(open(self.__default_prob_p, "rb"))

        logging.debug('Built probabilistic model in: %f', (time.time() - start_time))

    def calculate_probabilities(self, k=1):
        """Use Laplace smoothing to calculate the probabilities"""
        unigrams_count = functools.reduce(lambda v,e: v + e['count'], self.unigrams.values(), 0)
        num_unigrams = len(self.unigrams)

        for unigram in self.unigrams.values():
            unigram["p"] = (unigram["count"] + k) / (unigrams_count + k * num_unigrams)

        self.default_prob = {"count": 0, "p": k / (unigrams_count + k * num_unigrams)}
        pickle.dump(self.default_prob, open(self.__default_prob_p, "wb"))

    def probability(self, unigram):
        """Get the probability of the specified unigram"""
        try:
            return self.unigrams[unigram]["p"]
        except KeyError:
            return self.default_prob["p"]

def most_probable(text=TEXT, cols=19, rows=8):
    word_model = WordUnigrams()
    results = []

    # Pick admissible columns for the first one, figure out the best order for
    # each, and choose the one with the highest probability
    for i in range(cols):
        shuffled_text = ShuffledText(text=text, unigrams=word_model, cols=cols, rows=rows)
        start_col = shuffled_text.remove_column(i)
        # Discard columns that have rows that start with spaces
        if [r for r in start_col if r.startswith(' ')]:
            results.append((float("-inf"), None))
            continue

        ordered_text = ShuffledText(columns=[start_col], cols=1, rows=rows,
                text=None, unigrams=word_model)

        for j in range(1, cols):
            probabilities = []

            for c in range(len(shuffled_text.columns)):
                ordered_text.append_column(shuffled_text.column(c))
                temp_p = ordered_text.calculate_probability()
                ordered_text.remove_column(j)
                probabilities.append((temp_p, c))

            probabilities = sorted(probabilities, key=lambda val: val[0], reverse=True)
            logging.debug("Best probability (log(p)): %s", probabilities[0][0])
            ordered_text.append_column(shuffled_text.remove_column(probabilities[0][1]))

        results.append((ordered_text.calculate_probability(), ordered_text))

    return sorted(results, key=lambda res: res[0], reverse=True)

def main():
    sorted_results = most_probable()
    logging.debug(sorted_results)

    print(sorted_results[0][1])

if __name__ == "__main__":
    main()
