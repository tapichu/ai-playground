#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

"""
Use a probabilistic letter model to 'break' a rotation cipher.

This solution uses a very simple model (but it's enough to decode the message):
    * 2 letter bigrams built from a list of words (around 260,000 words).
    * Naïve Bayes assumption: P(bg_1, bg_2... bg_n) = Product(i:1..n) P(bg_i).

Requirements:
    * Python 3.x
"""

import functools
import logging
import os.path
import pickle
import re
import time

# Logging level
logging.basicConfig(level=logging.INFO)


# Text we're trying to decode
TEXT = "Esp qtcde nzyqpcpynp zy esp ezatn zq Lcetqtntlw \
Tyepwwtrpynp hld spwo le Olcexzfes Nzwwprp ty estd jplc."

ALPHABET_EN = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]


class RotationCipher:
    """Rotates character strings"""

    def __init__(self, alphabet=ALPHABET_EN, valid_chars="[a-z]"):
        self.alphabet = alphabet
        self.valid_chars = re.compile(valid_chars)

    def rotate_char(self, char, shift=0):
        """Map from one character to another by a shift of size N"""
        if self.valid_chars.match(char):
            char = self.alphabet[(self.alphabet.index(char) + shift) % len(self.alphabet)]
        return char

    def encode(self, text="", shift=0):
        """Map a string to another by a shift of size N"""
        return "".join([self.rotate_char(c, shift) for c in text.lower()])


class LetterBigrams:
    """Create letter bigrams from a word list"""

    def __init__(self, alphabet=ALPHABET_EN):
        self.alphabet = alphabet

        cwd = os.path.dirname(__file__)
        self.__words_file = os.path.join(cwd, "sowpods.txt")
        self.__words_p = os.path.join(cwd, ".words.p")
        self.__prob_model_p = os.path.join(cwd, ".prob_letter_model.p")

        if os.path.isfile(self.__words_p):
            self.words = pickle.load(open(self.__words_p, "rb"))
        else:
            self.words = []
            # TODO: get a better corpus, not just words, but real texts
            with open(self.__words_file, "r") as f:
                for line in iter(f.readline, ''):
                    self.words.append(line.lower().rstrip())
                pickle.dump(self.words, open(self.__words_p, "wb"))

        if os.path.isfile(self.__prob_model_p):
            self.bigrams = pickle.load(open(self.__prob_model_p, "rb"))
        else:
            self.build_probabilistic_model()
            pickle.dump(self.bigrams, open(self.__prob_model_p, "wb"))

    def build_probabilistic_model(self):
        """Create letter bigrams, count their ocurrences and calculate their probabilities"""
        start_time = time.time()

        words = ' '.join(self.words)
        # TODO: could make it generic, for N-grams, with itertools.permutations
        self.bigrams = [x + y for x in self.alphabet for y in self.alphabet]
        self.bigrams = dict([(x, {"count": words.count(x), "p": 0}) for x in self.bigrams])

        self.calculate_probabilities()

        logging.debug('Built probabilistic model in: %f', (time.time() - start_time))

    def calculate_probabilities(self, k=2):
        """Use Laplacian smoothing to calculate the probabilities"""
        bigrams_count = functools.reduce(lambda v,e: v + e['count'], self.bigrams.values(), 0)

        for bigram in self.bigrams.values():
            bigram["p"] = (bigram["count"] + k) / (bigrams_count + k)

    def probability(self, bigram):
        """Get the probability of the specified bigram"""
        return self.bigrams[bigram]["p"]


def most_probable(phrases):
    bigrams = LetterBigrams()
    best_phrase = ""
    best_p = 0
    second_best_p = 0

    for phrase in phrases:
        logging.debug("Phrase: %s", phrase)

        # Get all bigrams from the phrase, ignore the ones with spaces
        phrase_bigrams = [phrase[i:i+2] for i in range(0, len(phrase) - 1) if phrase[i:i+2].find(' ') == -1]
        logging.debug("Bigrams: %s", " ".join(phrase_bigrams))

        probability = functools.reduce(lambda v,e: v * bigrams.probability(e), phrase_bigrams, 1)
        logging.debug("Probability: %.4e", probability)

        if probability > best_p:
            best_phrase = phrase
            second_best_p = best_p
            best_p = probability
        elif probability > second_best_p:
            second_best_p = probability

    # TODO: return a list of (phrase, probability) sorted by their probability
    return (best_phrase, best_p, second_best_p)

def main():
    # Text cleanup: remove punctuation characters, etc.
    text = re.sub("[^a-z ]", "", TEXT.lower())

    rotation_cipher = RotationCipher()
    all_phrases = (rotation_cipher.encode(text, x) for x in range(0, 26))

    # Figure out the probability of each possible shift
    phrase, best_p, second_best_p = most_probable(all_phrases)
    print("Most probable phrase: %s" % phrase)
    print("With probability: %.4e" % best_p)
    print("Second best probability: %.4e" % second_best_p)

if __name__ == "__main__":
    main()
