"""
wordle.py
Contains a class that simulates the game of Wordle; used for problems 5-7.
Note to students: your code goes in information_theory.py, not this file.
"""

import numpy as np
import cmd

def load_words(filen):
    with open(filen, 'r') as file:
        # Get all 5-letter words
        words = [line.strip() for line in file.readlines() if len(line.strip()) == 5]
    return words

class WordleGame(cmd.Cmd):
    def __init__(self, allowed_fn='allowed_guesses.txt', possible_fn='possible_secret_words.txt'):
        self.allowed_words = load_words(allowed_fn)
        self.possible_words = load_words(possible_fn)
        self.word = None
        self._game_finished = False
        
    