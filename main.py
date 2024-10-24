"""
Program to build files holding functions for usage in other Python applications.
"""

import argparse
import os

current_path = os.getcwd()    # Get and store current working directory

def test_pass(message:="current test",verbose=False):
    """
    Function prints a message if it is executed. Purely for testing and debugging.

    Parameters:
    -----------
    - message: (str) Message to print. Default is 'current test'.
    - verbose: (bool) Determines whether or not to print a message. Default value is False.

    Returns:
    --------
    None
    """

    try:
        if verbose == True:
            final_print = "Test condition: " + str(message)
    except:
        print("Invalid value passed to function. Exiting.")

def main(verbose=False):
    pass

if __name__ == "__main__":
    main()
    # Test