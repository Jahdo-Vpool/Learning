import os
import time

def clear_screen():
    """Clears the screen in either a terminal or a Jupyter Notebook."""
    try:
        # This is for Jupyter Notebooks
        from IPython.display import clear_output
        clear_output(wait=True)
    except ImportError:
        # This is for standard terminals
        os.system('cls' if os.name == 'nt' else 'clear')

def print_separator():
    """Prints a separator line for better visual organization."""
    print("\n" + "=" * 100 + "\n")

def typewriter_effect(text, delay=0.03):
    """Prints text with a typewriter effect for a better user experience."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()