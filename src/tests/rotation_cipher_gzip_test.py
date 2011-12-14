#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

from .. import rotation_cipher_gzip as rcgzip
import unittest

class TestRotationCipherGzip(unittest.TestCase):

    def setUp(self):
        self.rc = rcgzip.RotationCipher()
        self.phrase = "Your highness, when I said that you are like a stream of bat's \
piss, I only mean that you shine out like a shaft of gold when all around it is dark"
        self.encoded_phrase = self.rc.encode(self.phrase, 5)

    def test_run_command(self):
        self.assertEqual(rcgzip.run_command('echo "10"'), 10)

    def test_run_command_error(self):
        self.assertEqual(rcgzip.run_command('not_found'), -1)

    def test_most_probable(self):
        phrases = [self.rc.encode(self.encoded_phrase, x) for x in range(0, 26)]
        phrase = rcgzip.most_probable(phrases)
        self.assertEqual(phrase, self.phrase.lower())

if __name__ == '__main__':
    unittest.main()
