# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 22:06:33 2022

@author: brigh

The purpose of this file is to provide easy solutions for input error handling

"""


class LengthError(Exception):
    pass


class badInputError(Exception):
    pass


def int_only_input(inputString):
    """


    Args:
        inputString (str): Will be displayed and prompt input
        varName (str): Name of the variable returned

    Returns:
        a global variable with the name defined by varName

    """
    tryLoop = True
    while tryLoop == True:
        try:
            var = int(input(inputString))
            return var
            tryLoop = False
        except ValueError:
            print("integers only")


def words_only_input(inputString):

    tryLoop = True
    while tryLoop == True:
        numbers = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"]
        try:
            var = input(inputString)

            for character in var:
                if character in numbers:
                    raise ValueError
                else:
                    pass
            return var
            tryLoop = False

        except ValueError:
            print("Words only")


def int_only_input_length(inputString, length):
    """
    Args:
        inputString (str): This will be displayed to the user and require a response
        varName (str): This is the name of the variable created by the user input
        length (int): The length of the input.

    Raises:
        LengthError: a suitable message for incorrect input length.

    Returns:
        A global integer of a pre-specified length.
    """
    tryLoop = True
    while tryLoop == True:
        try:
            var = int(input(inputString))
            testString = str(var)
            if len(testString) != length:
                raise LengthError()
            return var
            tryLoop = False
        except ValueError:
            print("integers only")
        except LengthError:
            print("LengthError - your input contains an invalid number of characters")


def yes_no(inputString):
    tryLoop = True
    while tryLoop == True:
        try:
            var = input(inputString+"[y/n]: ").lower()

            if var not in ["y", "n"]:
                raise badInputError

            return var
            tryLoop = False

        except badInputError:
            print("(y) or (n) only")
