import numpy as np
from collections import Counter
import json

# Helper functions
def load_words(filen: str):
    """
    Loads all of the words from the given file, ensuring that they
    are formatted correctly.
    """
    with open(filen, "r") as file:
        # Get all 5-letter words
        words = [line.strip() for line in file.readlines() if len(line.strip()) == 5]
    return words


def load_json(filen: str):
    """
    Loads the JSON file into a Python map.
    """
    with open(filen, "r") as file:
        data = json.load(file)
    return data


def get_guess_result(guess: str, true_word: str):
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


def hard_mode_file(possible_secret_words: list):
    """
    Creates the npy file showing every possible outcome of every possible secret word

    Arguments:
        possible_secret_words (list) - the list of all possible Wordle answers
    """
    m = len(possible_secret_words)
    hard_mode = np.zeros((m, m))
    for row in range(m):
        for col in range(m):
            guess_result = get_guess_result(
                possible_secret_words[row], possible_secret_words[col]
            )
            result_number = 0
            iter = 0
            for i in guess_result:
                result_number += i * (3**iter)
                iter += 1
            hard_mode[row][col] = result_number
    np.save("all_guess_results", hard_mode)

def save_text_file(words: list, filename: str):
    """
    Saves a list of words as a .txt file
    """
    with open(filename, 'w') as file:
        file.writelines(words)

def filter_files():
    # create the lists we need to work with 
    probability_map: dict = load_json("freq_map.json")
    allowed_guesses = np.array(probability_map.keys())
    frequencies = np.array(probability_map.values())
    # TODO: filter out plural words 
    # ending_with_s = [word[-1] == 's' for word in allowed_guesses ]

    index_array = np.argsort(frequencies)[::-1]
    most_common_words = []
    for i in index_array[:4500]:
        most_common_words.append(allowed_guesses[i] + "\n")
    save_text_file(most_common_words, "filtered_words.txt")
