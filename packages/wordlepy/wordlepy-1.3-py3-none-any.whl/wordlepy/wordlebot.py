import random
import time
import os
import pandas as pd

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# local imports
import wordle_class


def get_starting_word():
    """
    get random starting word from the frequently spoken word list.

    Returns
    -------
    word : TYPE
        DESCRIPTION.

    """

    # get starting word from common words list
    df = pd.read_excel(
        os.path.dirname(__file__) + "/frequency_list.xlsx", sheet_name=2, skiprows=1
    )

    df.drop_duplicates(inplace=True)

    df = df.astype({"LEMMA": "string"})

    df.dropna(inplace=True)

    word_list = df["LEMMA"].to_list()

    five_letter_words = [x.lower() for x in word_list if len(x.strip()) == 5]

    word = five_letter_words[random.randint(0, len(five_letter_words)) - 1]

    word = wordle_class.Word(word)

    return word


def submit_word(driver, word):
    """
    type word into webbrowser using webdriver

    Parameters
    ----------
    driver : TYPE
        DESCRIPTION.
    word : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    for letter in word.word:
        # random time interval between letters for fun
        time.sleep(random.randint(0, 25) * 0.01)
        webdriver.ActionChains(driver).send_keys(letter).perform()

    time.sleep(0.5)
    # send an enter key to submit word
    webdriver.ActionChains(driver).send_keys(Keys.ENTER).perform()


def check_results(driver, guess_word, rownum):
    """
    scan through the wordle tiles' css state
    Parameters
    ----------
    driver : TYPE
        DESCRIPTION.
    guess_word : TYPE
        DESCRIPTION.
    rownum : TYPE
        DESCRIPTION.

    Returns
    -------
    True or False is the guessed word is valid

    """

    return_code = True

    # each wordle tile is a span. find all spans
    spans = driver.find_elements(By.XPATH, "//span")

    # target the 5 letters on the correct row per guess:
    row = spans[(rownum - 1) * 5 : rownum * 5]

    for index, span in enumerate(row):
        if span.text.lower() == guess_word.word[index]:

            # use the latest css class state to determine
            # the letter state of each guessed letter, then
            # set the wordle Word object letter states
            if "nm-inset-n-gray" in span.get_attribute("class"):
                guess_word.letters[index].state = "wrong"

            elif "nm-inset-yellow" in span.get_attribute("class"):
                guess_word.letters[index].state = "misplaced"

            elif "nm-inset-n-green" in span.get_attribute("class"):
                guess_word.letters[index].state = "right"

            elif "border-red" in span.get_attribute("class"):
                print("invalid wordle word or character")
                return_code = False
            else:
                print("unknown state? race condition?")

    # next handle duplicates
    for letter in guess_word.letters:
        for other_letter in guess_word.letters:
            if (
                letter.letter == other_letter.letter
                and letter.state != other_letter.state
            ):
                if letter.state == "wrong":
                    letter.state = "misplaced"
                elif other_letter.state == "wrong":
                    other_letter.state = "misplaced"

    return return_code


def main(starting_wordle_num):
    """
    main entry point to program
    starts at "starting_wordle_num"
    then iterates through wordles in reverse until
    all wordles have been processed.

    Parameters
    ----------
    starting_wordle_num : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """

    for wordle_num in reversed(range(1, starting_wordle_num+1)):

        driver = webdriver.Chrome()
        # implicit 10 second wait added for full DOM/session
        driver.implicitly_wait(10)

        # browse to the wordle archive for a given wordle number
        driver.get(f"https://www.devangthakkar.com/wordle_archive/?{wordle_num}")

        # send an escape key to clear the how-to (if visible)
        webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()

        # print wordle header
        try:
            header = driver.find_element(By.XPATH, "//h1")
            print(header.text)
        except:
            print("no header to find")

        # get starting word returns a Wordle word class
        # the 5 letter guess word will be randomly chosen from
        # frequently spoken words in the word_frequency.xlsx
        starting_word = get_starting_word()

        print(f"starting with {starting_word.upper()}")

        # type word into wordle page
        submit_word(driver, starting_word)

        # check wordle results for a given guess word
        # the wordle Class object letter states are updated
        # accordingly
        while True:
            rc = check_results(driver, starting_word, rownum=1)
            # a -1 return code signifies an invalid wordle
            # in that case, backspace and retry
            if rc is False:
                print(f"{starting_word.word} is invalid! Clearing it out now")
                time.sleep(1)
                for i in range(6):
                    # clear out tiles with slight delay
                    webdriver.ActionChains(driver).send_keys(Keys.BACKSPACE).perform()
                    time.sleep(0.10)

                # get new word and try again
                starting_word = get_starting_word()
                print(f"Guessing {starting_word} from starting retry loop")
                submit_word(driver, starting_word)
            else:
                break

        for letter in starting_word.letters:
            print(f"{letter.letter} - {letter.state}")

        # read full list of possible words for subsequent guessing
        with open(os.path.dirname(__file__) + "/words_alpha.txt", "r") as words_file:
            all_words = words_file.readlines()

        five_letter_words = [x.lower() for x in all_words if len(x.strip()) == 5]

        # get remaining words list with our results of the starting word:
        remaining_word_list = wordle_class.get_remaining_words(
            five_letter_words, starting_word
        )

        print(f"{len(remaining_word_list)} remain for words")

        # init guess word as starting word
        guess_word = starting_word

        # iterate up to five more times while reducing the list
        for i in range(2, 7):

            # check to see if solved
            guess_word.check_if_solved()

            # yes, this is redundant..
            if guess_word.solved:
                print(f"{guess_word.word} is the answer!")
                break

            time.sleep(1)

            # guess random word from remaining
            # TODO: factor in LEMMA score to make better guesses
            if len(remaining_word_list) > 0:
                guess_word = remaining_word_list[
                    random.randint(0, len(remaining_word_list)) - 1
                ]

                print(f"Guessing {guess_word}")

                # convert to wordle word
                guess_word = wordle_class.Word(guess_word)

                # type in word:
                submit_word(driver, guess_word)

                # then drop into check results loop
                while True:
                    rc = check_results(driver, guess_word, rownum=i)
                    if rc is False:
                        print(f"{guess_word.word} is invalid! Clearing it out now")
                        time.sleep(1)
                        for j in range(6):
                            webdriver.ActionChains(driver).send_keys(
                                Keys.BACKSPACE
                            ).perform()
                            time.sleep(0.10)

                        # remove the incorrect word
                        remaining_word_list.remove(guess_word.word)

                        # guess a new word
                        guess_word = remaining_word_list[
                            random.randint(0, len(remaining_word_list)) - 1
                        ]

                        print(f"guessing {guess_word} from main retry loop")

                        # convert to wordle word
                        guess_word = wordle_class.Word(guess_word)
                        submit_word(driver, guess_word)
                    else:
                        break

                time.sleep(1)

                # check if word solved
                if guess_word.check_if_solved():
                    print(f"{guess_word.word} is the answer!")
                    with open("wordlebot_solutions.txt", "w") as solution_file:
                        solution_file.write(f"{wordle_num},{guess_word.word}\n")

                    # break out of guessing for loop
                    # continue main loop for next wordle
                    # after appending answer to text file
                    break

                # remove this guess from the list
                remaining_word_list.remove(guess_word.word)

                remaining_word_list = wordle_class.get_remaining_words(
                    remaining_word_list, guess_word
                )

                print(f"{len(remaining_word_list)} remain(s)")

            elif len(remaining_word_list) == 1:
                print("one word remains! return.")
                break

            else:
                print("out of letters to chose from... hmmm")
                break


if __name__ == "__main__":
    # pick starting wordle
    starting_wordle_num = 271
    main(starting_wordle_num)
