# This file contains small, reusable helper functions to improve the game's user interface and experience.
import os
import time

def clear_screen():
    """Clears the screen in either a terminal or a Jupyter Notebook."""
    # This function provides a cross-platform way to clear the console screen.
    # It first tries the method for Jupyter/IPython environments.
    try:
        from IPython.display import clear_output
        # The 'wait=True' argument is important to prevent flickering in loops.
        clear_output(wait=True)
    # If the IPython library isn't found, it means we're likely in a standard terminal.
    except ImportError:
        # 'os.name' checks the operating system. 'nt' is for Windows.
        # It then runs the appropriate shell command ('cls' or 'clear') to clear the screen.
        os.system('cls' if os.name == 'nt' else 'clear')


def print_separator():
    """Prints a separator line for better visual organization."""
    # This function improves readability by visually breaking up sections of text.
    # The number 100 can be changed to make the separator line longer or shorter.
    print("\n" + "=" * 100 + "\n")

def typewriter_effect(text, delay=0.03):
    """Prints text with a typewriter effect for a better user experience."""
    # This loop iterates over every single character in the provided text string.
    for char in text:
        # The 'end=""' argument prevents the print function from adding a newline at the end,
        # which keeps all characters on the same line.
        # The 'flush=True' argument forces the output to be displayed immediately,
        # which is essential for the character-by-character effect.
        print(char, end='', flush=True)

        # time.sleep() pauses the program for a tiny fraction of a second to control the typing speed.
        time.sleep(delay)

    # After the loop has finished printing all characters, this prints a final newline
    # to move the cursor down for the next line of output.
    print()