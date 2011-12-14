#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "MIT License"

"""
Use a probabilistic letter model to break a rotation cipher.
"""

TEXT = "Esp qtcde nzyqpcpynp zy esp ezatn zq Lcetqtntlw \
Tyepwwtrpynp hld spwo le Olcexzfes Nzwwprp ty estd jplc."

class RotationCipher:
    """Rotates character strings"""

    def __init__(self):
        self.alphabet = [
            "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
            "n", "o", "p", "q", "r", "s", "t", "u", "v", "w", "x", "y", "z"
        ]

    def rotate_char(self, char, shift=0):
        """Map from one character to another by a shift of size N"""
        return self.alphabet[(self.alphabet.index(char) + shift) % len(self.alphabet)]

    def cipher(self, text="", shift=0):
        """Map a string to another by a shift of size N"""
        char_list = list(map(lambda c: self.rotate_char(c, shift), text.lower()))
        return "".join(char_list)

if __name__ == "__main__":
    print(TEXT)
