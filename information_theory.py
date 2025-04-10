"""
Information Theory Lab

Sarah Winters
Section 001
"""


import numpy as np
import wordle
from collections import Counter
import random

# Problem 1
def get_guess_result(guess, true_word):
    """
    Returns an array containing the result of a guess, with the return values as follows:
        2 - correct location of the letter
        1 - incorrect location but present in word
        0 - not present in word
    For example, if the secret word is "boxed" and the provided guess is "excel", the 
    function should return [0,1,0,2,0].
    
    Arguments:
        guess (string) - the guess being made
        true_word (string) - the secret word
    Returns:
        result (list of integers) - the result of the guess, as described above
    """
    # define the result as an array of size 5
    length = 5
    correct_loc = 2
    in_word = 1
    not_present = 0
    result = np.zeros(length)
    repeated = Counter(true_word)
    # turn strings into lists
    answer_list = [l for l in true_word]
    guess_list = [w for w in guess]

    # we account for the letters that aren't in the word by initializing it at 0
   
    # now we need to see if the letters match in the exact same place
    for i in range(length):
        if guess_list[i] == answer_list[i]:
            result[i] = correct_loc
            repeated[guess_list[i]] -= 1
    
    # we have to accout for repeated letters and letters in a different place 
    for i in range(length):
        if result[i] != correct_loc:
            # this is for letters that are in the word but aren't in the right place
            letter = guess_list[i]
            if repeated[letter] == 1:
                result[i] = in_word
            if repeated[letter] > 1:
                result[i] = in_word
            repeated[letter] -= 1
    return result

# Helper function
def load_words(filen):
    """
    Loads all of the words from the given file, ensuring that they 
    are formatted correctly.
    """
    with open(filen, 'r') as file:
        # Get all 5-letter words
        words = [line.strip() for line in file.readlines() if len(line.strip()) == 5]
    return words
    
# Problem 2
def compute_highest_entropy(all_guess_results, allowed_guesses):
    """
    Compute the entropy of each allowed guess.
    
    Arguments:
        all_guess_results ((n,m) ndarray) - the array found in
            all_guess_results.npy, containing the results of each 
            guess for each secret word, where n is the the number
            of allowed guesses and m is number of possible secret words.
        allowed_guesses (list of strings) - list of the allowed guesses
    Returns:
        (string) The highest-entropy guess
    """
    num_guesses, num_secrets = all_guess_results.shape
    # initialize a list of entropy values
    entropy = np.empty(num_guesses)
    # loop through allowed_guesses
    for i in range(num_guesses):
        secret_words = all_guess_results[i]
        void, count = np.unique(secret_words, return_counts=True)
        frequency = count / num_secrets
        # calculate entropy
        entropy[i] = np.sum([-1 * prob * np.log2(prob) for prob in frequency])

    # find the argmax to get the correct guess with highest entropy
    index = np.argmax(entropy)
    return allowed_guesses[index]

    
# Problem 3
def filter_words(all_guess_results, allowed_guesses, possible_secret_words, guess, result):
    """
    Create a function that filters the list of possible words after making a guess.
    Since we already have an array of the result of all guesses for all possible words, 
    we will use this array instead of recomputing the results.
    
	Return a filtered list of possible words that are still possible after 
    knowing the result of a guess. Also return a filtered version of the array
    of all guess results that only contains the results for the secret words 
    still possible after making the guess. This array will be used to compute 
    the entropies for making the next guess.
    
    Arguments:
        all_guess_results (2-D ndarray)
            The array found in all_guess_results.npy, 
            containing the result of making any allowed 
            guess for any possible secret word
        allowed_guesses (list of str)
            The list of words we are allowed to guess
        possible_secret_words (list of str)
            The list of possible secret words
        guess (str)
            The guess we made
        result (tuple of int)
            The result of the guess
    Returns:
        (list of str) The filtered list of possible secret words
        (2-D ndarray) The filtered array of guess results
    """
    # first find the row of our guess in all_guess_results
    guess_index = allowed_guesses.index(guess)
    guess_row = all_guess_results[guess_index]
    # find the corresponding secret words that work with our result
    result_number = 0
    iter = 0
    # change our result to the desired format
    for i in result:
        result_number += i* (3**iter)
        iter += 1
    mask = guess_row == result_number

    new_secrets = np.array(possible_secret_words)[mask]
    # now apply the mask to the 2d array
    new_array = all_guess_results[:, mask]
    return list(new_secrets), new_array


# Problem 4
def play_game_naive(game, all_guess_results, possible_secret_words, allowed_guesses, word=None, display=False):
    """
    Plays a game of Wordle using the strategy of making guesses at random.
    
    Return how many guesses were used.
    
    Arguments:
        game (wordle.WordleGame)
            the Wordle game object
        all_guess_results ((n,m) ndarray)
            The array found in all_guess_results.npy, 
            containing the result of making any allowed 
            guess for any possible secret word
        possible_secret_words (list of str)
            list of possible secret words
        allowed_guesses (list of str)
            list of allowed guesses
        
        word (optional)
            If not None, this is the secret word; can be used for testing. 
        display (bool)
            If true, output will be printed to the terminal by the game.
    Returns:
        (int) Number of guesses made
    """
    # Initialize the game
    game.start_game(word=word, display=display)
    guesses = 0
    while not game.is_finished():
        # if there is only one choice left
        if len(possible_secret_words) == 1:
            result, guesses = game.make_guess(possible_secret_words[0])
            return guesses
        # create the necessary parameters
        guess = random.choice(allowed_guesses)
        result, guesses = game.make_guess(guess)
        # call previous function to filter results
        possible_secret_words, all_guess_results = filter_words(all_guess_results, allowed_guesses, 
                                                                possible_secret_words, guess, result)
    # return the number of guesses made
    return guesses

# Problem 5
def play_game_entropy(game, all_guess_results, possible_secret_words, allowed_guesses, word=None, display=False):
    """
    Plays a game of Wordle using the strategy of guessing the maximum-entropy guess.
    
    Return how many guesses were used.
    
    Arguments:
        game (wordle.WordleGame)
            the Wordle game object
        all_guess_results ((n,m) ndarray)
            The array found in all_guess_results.npy, 
            containing the result of making any allowed 
            guess for any possible secret word
        possible_secret_words (list of str)
            list of possible secret words
        allowed_guesses (list of str)
            list of allowed guesses
        
        word (optional)
            If not None, this is the secret word; can be used for testing. 
        display (bool)
            If true, output will be printed to the terminal by the game.
    Returns:
        (int) Number of guesses made
    """
    game.start_game(word=word, display=display)
    guesses = 0
    while not game.is_finished():
        # if there is only one choice left
        if len(possible_secret_words) == 1:
            result, guesses = game.make_guess(possible_secret_words[0])
            return guesses
        # create the necessary parameters
        # use the highest entropy word as your guess
        guess = compute_highest_entropy(all_guess_results, allowed_guesses)
        result, guesses = game.make_guess(guess)
        
        # call previous function to filter results
        possible_secret_words, all_guess_results = filter_words(all_guess_results, allowed_guesses, 
                                                                possible_secret_words, guess, result)
    # return the number of guesses made
    return guesses


# Problem 6
def compare_algorithms(all_guess_results, possible_secret_words, allowed_guesses, n=20):
    """
    Compare the algorithms created in Problems 5 and 6. Play n games with each
    algorithm. Return the mean number of guesses the algorithms from
    problems 5 and 6 needed to guess the secret word, in that order.
    
    
    Arguments:
        all_guess_results ((n,m) ndarray)
            The array found in all_guess_results.npy, 
            containing the result of making any allowed 
            guess for any possible secret word
        possible_secret_words (list of str)
            list of possible secret words
        allowed_guesses (list of str)
            list of allowed guesses
        n (int)
            Number of games to run
    Returns:
        (float) - average number of guesses needed by naive algorithm
        (float) - average number of guesses needed by entropy algorithm
    """
    game = wordle.WordleGame()
    random_guesses = sum([play_game_naive(game, all_guess_results, possible_secret_words, 
                                      allowed_guesses, word=None, display=False) for i in range(n)])/n
    entropy_guesses = sum([play_game_entropy(game, all_guess_results, possible_secret_words, 
                                      allowed_guesses, word=None, display=False) for i in range(n)])/n
    return random_guesses, entropy_guesses
