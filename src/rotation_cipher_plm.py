#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "MIT License"

"""
Use a probabilistic letter model to break a rotation cipher.
"""

import functools
import logging
import os
import time

# Logging level
logging.basicConfig(level=logging.DEBUG)

TEXT = "Esp qtcde nzyqpcpynp zy esp ezatn zq Lcetqtntlw \
Tyepwwtrpynp hld spwo le Olcexzfes Nzwwprp ty estd jplc."

ALPHABET_EN = [
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
]

class RotationCipher:
    """Rotates character strings"""

    def __init__(self, alphabet=ALPHABET_EN):
        self.alphabet = alphabet

    def rotate_char(self, char, shift=0):
        """Map from one character to another by a shift of size N"""
        return self.alphabet[(self.alphabet.index(char) + shift) % len(self.alphabet)]

    def cipher(self, text="", shift=0):
        """Map a string to another by a shift of size N"""
        return "".join([self.rotate_char(c, shift) for c in text.lower()])

class LetterBigrams:
    """Create letter bigrams from a word list"""

    def __init__(self, alphabet=ALPHABET_EN):
        self.alphabet = alphabet

        self.words = []
        with open(os.path.join(os.path.dirname(__file__), "sowpods.txt")) as f:
            for line in iter(f.readline, ''):
                self.words.append(line.lower().rstrip())

        self.build_probabilistic_model()

    def build_probabilistic_model(self):
        start_time = time.time()

        words = ' '.join(self.words)
        # TODO: could make it generic, for N-grams, with itertools.permutations
        self.bigrams = [x + y for x in self.alphabet for y in self.alphabet]
        self.bigrams = dict([(x, {"count": words.count(x), "p": 0}) for x in self.bigrams])

        self.bigrams_count = functools.reduce(lambda v,e: v + e['count'], self.bigrams.values(), 0)

        logging.debug('Built probabilistic model in: %f', (time.time() - start_time))

def main():
    # Figure out the probability of each possible shift
    rotation_cipher = RotationCipher()
    [rotation_cipher.cipher(TEXT, x) for x in range(0, 26)]

if __name__ == "__main__":
    print(TEXT)
