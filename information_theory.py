import numpy as np
import utils


def compute_highest_entropy(all_guess_results, allowed_guesses, probability_map):
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
    num_guesses = all_guess_results.shape[0]
    # initialize a list of entropy values
    entropy = np.empty(num_guesses)
    # loop through allowed_guesses
    for i in range(num_guesses):
        secret_words = all_guess_results[i]
        void, count = np.unique(secret_words, return_counts=True)
        frequency = count / num_guesses
        # calculate entropy
        entropy[i] = np.sum([-1 * prob * np.log2(prob) for prob in frequency])

    # find the argmax to get the correct guess with highest entropy
    index = np.argmax(entropy)
    return allowed_guesses[index]


# Problem 3
def filter_words(
    all_guess_results, possible_secret_words, probability_map, guess, result
):
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
    guess_index = possible_secret_words.index(guess)
    guess_row = all_guess_results[guess_index]
    # find the corresponding secret words that work with our result
    result_number = 0
    iter = 0
    # change our result to the desired format
    for i in result:
        if type(i) == str:
            i = int(i)
        result_number += i * (3**iter)
        iter += 1
    mask = guess_row == result_number
    # create the new list and dictionary of the possible words
    new_secrets = np.array(possible_secret_words)[mask]
    new_probabilities = {k: probability_map[k] for k in new_secrets}
    # now apply the mask to the 2d array
    new_array = all_guess_results[mask]
    new_array = new_array[:, mask]
    return list(new_secrets), new_array, new_probabilities


def wordle_companion():
    """Function to run while playing Wordle. It will start by outputting the best first guess, then the
    user has to input their guess and the result of each guess to pass into `filter_words`
    """

    # load in the required files
    all_guess_results = np.load("all_guess_results.npy")
    allowed_guesses = utils.load_words("filtered_words.txt")
    probability_map = utils.load_json("freq_map.json")
    frequencies = dict()
    for word in allowed_guesses:
        frequencies[word] = probability_map[word]
    guess = compute_highest_entropy(all_guess_results, allowed_guesses, frequencies)

    # script
    print("Ready for another day of Wordle? Your first guess should be", guess)
    game_over = False
    num_guesses = 0
    while not game_over:
        num_guesses += 1
        correct_guess = input("Was that the word? (Y/N) ")
        if correct_guess == "Y" or correct_guess == "y" or num_guesses > 6:
            game_over = True
            break
        else:
            game_over = False
        # Get the results of the player's guess, formatted as a list of 0, 1, 2
        result = []
        incorrect_type = False
        while len(result) != 5 or incorrect_type:
            result = input(
                "What was your result? Please separate each value by a space. "
            ).split()
            if type(result) == int:
                incorrect_type = True
                print("The result must either be a string or a list")
        allowed_guesses, all_guess_results, probability_map = filter_words(
            all_guess_results, allowed_guesses, probability_map, guess, result
        )
        guess = compute_highest_entropy(
            all_guess_results, allowed_guesses, probability_map
        )
        print("Your next guess should be", guess)

    if num_guesses > 6:
        print("Better luck next time, champ")
    else:
        print(f"Great job! You solved wordle in {num_guesses} guesses!")
