#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "MIT License"

"""
Use a probabilistic letter model to break a rotation cipher.
"""

import os

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
        char_list = list(map(lambda c: self.rotate_char(c, shift), text.lower()))
        return "".join(char_list)

class LetterBigrams:
    """Create letter bigrams from a word list"""

    def __init__(self, alphabet=ALPHABET_EN):
        self.alphabet = alphabet

        self.words = []
        with open(os.path.join(os.path.dirname(__file__), "sowpods.txt")) as f:
            for line in iter(f.readline, ''):
                self.words.append(line.lower().rstrip())

        self.bigrams = [x + y for x in self.alphabet for y in self.alphabet]
        self.bigrams = dict([(x, {"count": 0, "p": 0}) for x in self.bigrams])

if __name__ == "__main__":
    print(TEXT)
