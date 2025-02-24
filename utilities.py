import os
import keyboard


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_input():
    input(keyboard.press_and_release("enter"))

def pick_resource(resource_list):
        max_resources = 9
        count = 0
        if len(resource_list) == 0:
            return -1
        for resource in resource_list:
            print("""
                 [{0}] - {1}""".format(count, resource))
            count += 1
            if max_resources > 9:
                break

        while 1:
            count = 0
            for resource in resource_list:
                if keyboard.is_pressed(str(count)):
                    return resource
                if keyboard.is_pressed('b'):
                    return -1
                count += 1

def do_quit():
    """Exit the CLI."""
    quit("\nThank you for using Tomer AWS resource manager!")
