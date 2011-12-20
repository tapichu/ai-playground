#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

"""
Use a probabilistic letter model to 'break' a rotation cipher.

This solution uses a very simple model (but it's enough to decode the message):
    * 2 letter bigram probabilities built from a list of words (around 260,000 words).
    * Naïve Bayes assumption: P(bg_1, bg_2... bg_n) = Product(i:1..n) P(bg_i).

Requirements:
    * Python 3.x
"""

from probabilistic_model import ProbabilisticModel
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


class LetterBigrams(ProbabilisticModel):
    """Create letter bigrams from a word list"""

    def __init__(self, alphabet=ALPHABET_EN):
        self.alphabet = alphabet
        cwd = os.path.dirname(__file__)
        self.__words_file = os.path.join(cwd, "sowpods.txt")
        self.__words_p = os.path.join(cwd, ".words.p")

        super().__init__(".prob_letter_model.p")

    def build_probabilistic_model(self):
        """Create letter bigrams, count their ocurrences and calculate their probabilities"""
        start_time = time.time()

        if os.path.isfile(self.__words_p):
            self.words = pickle.load(open(self.__words_p, "rb"))
        else:
            self.words = []
            with open(self.__words_file, "r") as f:
                for line in iter(f.readline, ''):
                    self.words.append(line.lower().rstrip())
                pickle.dump(self.words, open(self.__words_p, "wb"))

        words = ' '.join(self.words)
        # TODO: could make it generic, for N-grams, with itertools.permutations
        self.model = [x + y for x in self.alphabet for y in self.alphabet]
        self.model = dict([(bi, {"count": words.count(bi), "p": 0}) for bi in self.model])

        self.calculate_probabilities()
        logging.debug('Built probabilistic model in: %f', (time.time() - start_time))

    def calculate_probabilities(self, k=1):
        """Use Laplace smoothing to calculate the probabilities"""
        bigrams_count = functools.reduce(lambda v,e: v + e['count'], self.model.values(), 0)
        num_bigrams = len(self.model)

        for bigram in self.model.values():
            bigram["p"] = (bigram["count"] + k) / (bigrams_count + k * num_bigrams)

    def probability(self, bigram):
        """Get the probability of the specified bigram"""
        return self.model[bigram]["p"]


def most_probable(phrases):
    bigrams = LetterBigrams()
    results = []

    for phrase in phrases:
        logging.debug("Phrase: %s", phrase)

        # Get all bigrams from the phrase, ignore the ones with spaces
        phrase_bigrams = [phrase[i:i+2] for i in range(0, len(phrase) - 1) if phrase[i:i+2].find(' ') == -1]
        logging.debug("Bigrams: %s", " ".join(phrase_bigrams))

        probability = functools.reduce(lambda v,e: v * bigrams.probability(e), phrase_bigrams, 1)
        logging.debug("Probability: %.4e", probability)

        results.append((probability, phrase))

    return sorted(results, key=lambda val: val[0], reverse=True)

def main():
    # Text cleanup: remove punctuation characters, etc.
    text = re.sub("[^a-z ]", "", TEXT.lower())

    rotation_cipher = RotationCipher()
    all_phrases = (rotation_cipher.encode(text, x) for x in range(0, 26))

    # Figure out the probability of each possible shift
    sorted_phrases = most_probable(all_phrases)
    print("Most probable phrase: %s" % sorted_phrases[0][1])
    print("With probability: %.4e" % sorted_phrases[0][0])
    print("Second best probability: %.4e" % sorted_phrases[1][0])

if __name__ == "__main__":
    main()
