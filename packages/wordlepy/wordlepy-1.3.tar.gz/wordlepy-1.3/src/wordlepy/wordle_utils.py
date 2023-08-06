# -*- coding: utf-8 -*-
"""
Created on Thu Mar  3 10:33:39 2022

@author: bhook

helper utilities for wordle

"""

import random


def subwords_containing(wordlist, letters=["e", "t", "a", "s"]):
    """
    return a list of words containing the specified list of letters.

    Parameters
    ----------
    wordlist : TYPE
        DESCRIPTION.
    letters : TYPE, optional
        DESCRIPTION. The default is ["e", "t", "a", "s"].

    Returns
    -------
    return_list : TYPE
        DESCRIPTION.

    """

    return_list = list()
    match_count = len(letters)
    count = 0
    for word in wordlist:
        for letter in letters:
            if letter in word:
                count += 1
            else:
                break

        if count == match_count:
            return_list.append(word.strip())
            count = 0
        else:
            count = 0

    return return_list


def subwords_not_containing(wordlist, letters=[]):
    """
    return a list of words NOT containing the specified list of letters

    Parameters
    ----------
    wordlist : TYPE
        DESCRIPTION.
    letters : TYPE, optional
        DESCRIPTION. The default is [].

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    match_count = len(letters)
    count = 0
    return_list = list()
    for word in wordlist:
        for letter in letters:
            if letter not in word:
                count += 1
            else:
                break

        if count == match_count:
            return_list.append(word.strip())
            count = 0
        else:
            count = 0

    return sorted(return_list)


def letter_at_pos(wordlist, letter, pos):
    """
    return words containing the specifed letter at the specified position.

    Parameters
    ----------
    wordlist : TYPE
        DESCRIPTION.
    letter : TYPE
        DESCRIPTION.
    pos : TYPE
        DESCRIPTION.

    Returns
    -------
    return_list : TYPE
        DESCRIPTION.

    """
    return_list = list()
    for word in wordlist:
        if word[pos] == letter:
            return_list.append(word)

    return return_list


def letter_not_at_pos(wordlist, letter, pos):
    """
    return words NOT containing the specifed letter at the specified position.

    Parameters
    ----------
    wordlist : TYPE
        DESCRIPTION.
    letter : TYPE
        DESCRIPTION.
    pos : TYPE
        DESCRIPTION.

    Returns
    -------
    return_list : TYPE
        DESCRIPTION.

    """
    return_list = list()
    for word in wordlist:
        if word[pos] == letter:
            pass
        else:
            return_list.append(word)

    return return_list


def get_starting_word(five_letter_words, automated=False):
    """
    present the user with random words to start with.
    return the word

    Parameters
    ----------
    five_letter_words : TYPE
        DESCRIPTION.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """

    if automated:
        return five_letter_words[random.randint(0, len(five_letter_words)) - 1]

    else:
        while True:
            starting_word = five_letter_words[
                random.randint(0, len(five_letter_words)) - 1
            ]
            choice = input(
                f"Press [c] to continue with [{starting_word.upper()}] as your starting word, or enter to generate a new one: "
            ).strip()
            if choice.lower() == "c":
                return starting_word.strip()
