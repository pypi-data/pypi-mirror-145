# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:22:25 2022

@author: bhook

class implemtation of a wordle word.
each word consists of letters that have states from the game

unknown: untested letter
correct: (right letter, right position)
wrong: letter does not exist in the word
misplaced: (right letter, wrong position)

this module will allow the user to load ~all posible wordle solutions, pick a
random word if desired, then iterate through each word eliminating words each
step until a solution is found OR they run out of guesses.

"""


import wordle_utils
import pandas as pd
import os
import sys

# set the path so we can find our modules
sys.path.append(os.path.join(os.path.dirname(__file__)))


class Word:
    """
    Wordle word class that contains stateful letters
    and functions / status variables for signaling game state.
    """

    def __init__(self, word):
        """
        load in the guess word as a string
        init the members.

        Parameters
        ----------
        word : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.word = word
        self.letters = list()
        self.solved = False
        # set all letters to an unknown status initially
        for letter in word:
            self.letters.append(Letter(letter, "unknown"))

    def check_if_solved(self):
        """
        convienence function to check if solved
        (all letters have 'right' status)

        Returns
        -------
        None.

        """
        count = 0
        for letter in self.letters:
            if letter.state == "right":
                count += 1

        if count == 5:
            self.solved = True
            return True
        else:
            self.solved = False
            return False

    def upper(self):
        """
        convenience function to return uppercase
        version of word.word

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.word.upper()

    def lower(self):
        """
        convenience function to return lowercase
        version of word.word

        Returns
        -------
        TYPE
            DESCRIPTION.

        """
        return self.word.lower()

    def update(self):
        """
        instruct the user for setting each letter state to match
        the latest wordle result on a given attempt.

        Returns
        -------
        None.

        """
        print("For each letter enter: [r/w/m] for right, wrong, or misplaced")
        retry = False
        correct_count = 0
        for letter in self.letters:

            choice = input(f"{letter.letter}:")

            if choice == "r":
                letter.state = "right"
                correct_count += 1

            elif choice == "w":
                # check for duplicate letters that are 'right'
                # if they exist AND they have been marked right
                # change the current letter to 'misplaced' from 'wrong'
                dup_count = 0
                for sub_letter in self.letters:
                    if sub_letter.letter == letter.letter and (
                        sub_letter.state == "right" or sub_letter.state == "misplaced"
                    ):
                        dup_count += 1

                if dup_count > 1:
                    print(
                        "duplicate exists elsewhere in the word. 'w' is invalid. I changed your choice to 'misplaced' instead."
                    )
                    letter.state = "misplaced"
                else:
                    letter.state = "wrong"

            elif choice == "m":
                letter.state = "misplaced"

            else:
                print("Invalid choice. The only options are [r/w/m] try again.")
                retry = True
                self.update()
                # break out if the user has retried the input.
                if retry:
                    break

        if correct_count == 5:
            print("SOLVED!")
            self.solved = True


class Letter:
    """
    wordle letter with states
    """

    def __init__(self, letter, state):
        """
        letter is the alphabet characeter
        state refers to its "wordle state"

        Parameters
        ----------
        letter : TYPE
            DESCRIPTION.
        state : TYPE
            DESCRIPTION.

        Returns
        -------
        None.

        """
        self.letter = letter
        self.state = state


def get_remaining_words(word_list, word=Word):
    """
    filter the remaining word list by current letter(s) state
    of the passed Word object. return the new list.

    Parameters
    ----------
    word_list : TYPE
        DESCRIPTION.
    word : TYPE, optional
        DESCRIPTION. The default is Word.

    Returns
    -------
    word_list : TYPE
        DESCRIPTION.

    """

    for index, letter in enumerate(word.letters):

        if letter.state == "right":
            word_list = wordle_utils.letter_at_pos(word_list, letter.letter, index)
        elif letter.state == "wrong":
            word_list = wordle_utils.subwords_not_containing(word_list, [letter.letter])
        elif letter.state == "misplaced":
            word_list = wordle_utils.subwords_containing(word_list, [letter.letter])
            word_list = wordle_utils.letter_not_at_pos(word_list, letter.letter, index)

    return word_list


def main():
    """
    main entry point to the progam

    Returns
    -------
    None.

    """
    print("Loading full wordlist(s)...")

    # read in our full list of english words
    with open(os.path.dirname(__file__) + "/words_alpha.txt", "r") as words_file:
        words = words_file.readlines()

    # keep only the five letter words
    five_letter_words = list()

    for word in words:
        if len(word.strip()) == 5:
            five_letter_words.append(word.strip().lower())

    # Load list of common words to show a relative frequency
    try:
        df = pd.read_excel(
            os.path.dirname(__file__) + "/frequency_list.xlsx",
            sheet_name=2,
            skiprows=1,
            index_col=1,
        )
    except OSError:
        print("failed to find or load the the word frequency list.")
        print("setting the frequency list to an empty dataframe.")
        df = pd.DataFrame()

    df.drop_duplicates(inplace=False)

    # initialize the word list
    word_list = five_letter_words

    print(f"{len(word_list)} five letter words have been loaded. Done.")

    print("Removing prior wordle solutions from the list...")

    with open(os.path.dirname(__file__) + "/wordle_solutions.txt") as solutions_file:
        solutions = solutions_file.readlines()
        solutions = [solution.strip() for solution in solutions]

    for solution in solutions:
        try:
            # filter out blanks/whitespaces
            if len(solution) > 1:
                # remove each prior solution from the word list
                if solution in word_list:
                    word_list.remove(solution)
        except ValueError:
            print(
                f"[{solution}] from the solutions file doesnt appear in the word list."
            )
            print(
                "This shouldn't happen unless the solutions file was modified externally."
            )

    print(f"{len(word_list)} five letter words remain. Done.")

    # you get 6 tries...
    for i in range(6):

        # ask the user for their initial guess
        guess_word = input('Input your word (or type "random") then hit [ENTER]: ')

        # if the user accidentally selects the word index
        # select the word accompanying that number for them:
        if guess_word.isnumeric():
            guess_word = word_list[int(guess_word)]

        guess_word = guess_word.strip()

        if guess_word.lower() == "random":
            guess_word = wordle_utils.get_starting_word(word_list, automated=False)

        guess_word = guess_word.lower()

        assert len(guess_word) == 5, "Passed word must have 5 letters only."

        if guess_word in five_letter_words:

            # initialize wordle word class with guess word str
            word = Word(guess_word)

            print(f'Check "{word.word}" on Wordle then:\n')

            word.update()

            if word.solved:
                print(f"{word.word} is the answer! Congrats!")
                with open(
                    os.path.dirname(__file__) + "/wordle_solutions.txt", "a"
                ) as outfile:
                    # manually strip any newline chars
                    outword = word.word.strip()
                    # then append a windows line ending
                    outfile.write(outword + "\r\n")
                break
            else:
                # find new words from process of elimination()
                word_list = get_remaining_words(word_list, word)

                if len(word_list) > 0:

                    print("\nLatest words to chose from:")

                    for index, word in enumerate(word_list):
                        try:
                            print(
                                index, ". ", word, "\t", df.loc[word, "FREQUENCY"].max()
                            )
                        except KeyError:
                            print(index, ". ", word)
                else:
                    print("Out of words to guess. Double check your inputs.")

        else:
            if guess_word in solutions:
                print(f"[{guess_word}] is a previous solution. Try again. Exit.")
                break
            else:
                print(f"{guess_word} doesn't appear to be in the wordlist. Exit.")
                break


if __name__ == "__main__":
    main()
