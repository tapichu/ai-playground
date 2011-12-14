#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = "Eduardo Lopez Biagi"
__license__ = "BSD-new"

"""
Use gzip to 'break' a rotation cipher.

Concatenate each possible encoding (rotation) with a text in english.
Run this through gzip and count the number of characters in the output.
The smallest one should be the one in english.

Requirements:
    * Python 3.x
    * Basic UNIX commands: gzip, cat, echo, wc, sort, head, cut
"""

from rotation_cipher_plm import TEXT, RotationCipher
import logging
import os.path
import re
import subprocess

# Logging level
logging.basicConfig(level=logging.INFO)


def run_command(command):
    """Spawn a new process to execute a command on the shell"""
    proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout_value, stderr_value = proc.communicate()

    if proc.returncode > 1:
        logging.error(stderr_value)
        return -1
    else:
        logging.debug(stdout_value)
        return int(stdout_value)

def most_probable(phrases):
    """
    Build a command that runs each phrase through gzip. Select the phrase that produces the
    smallest gzip output (no. of characters).
    """
    idx = 0
    command = "("
    text_en = os.path.join(os.path.dirname(__file__), "text_en.txt")
    for phrase in phrases:
        command += 'echo `echo "%s $(cat %s)" | gzip | wc -c` %i; ' % (phrase, text_en, idx)
        idx += 1
    command += ") | sort -n | head -1 | cut -d ' ' -f 2"
    logging.debug("Command: %s", command)

    best_idx = run_command(command)
    return phrases[best_idx] if best_idx >= 0 else "An error occurred"

def main():
    # Text cleanup: remove punctuation characters, etc.
    text = re.sub("[^a-z ]", "", TEXT.lower())

    rotation_cipher = RotationCipher()
    all_phrases = [rotation_cipher.encode(text, x) for x in range(0, 26)]

    # Figure out the probability of each possible shift
    phrase = most_probable(all_phrases)
    print("Most probable phrase: %s" % phrase)

if __name__ == "__main__":
    main()
