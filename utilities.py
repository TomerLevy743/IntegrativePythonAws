import os
import keyboard


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_input():
    input(keyboard.press_and_release("enter"))

def do_quit():
    """Exit the CLI."""
    exit()
