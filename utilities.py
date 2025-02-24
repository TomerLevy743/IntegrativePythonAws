import os
import keyboard


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_input():
    input(keyboard.press_and_release("enter"))

def pick_resource(resource_list):
        print("Pick a resource to operate on:")
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
def get_key():
    return "Key"
def get_value():
    return "Value"



def cli_tags():
    return [
        {
            get_key(): 'by',
            get_value(): 'tomer-cli'
        },
        {
            get_key(): 'Owner',
            get_value(): 'tomerlevy'
        }
    ]
def filter_by_tags(resource_tags):

    key = "Key"
    value = "Value"
    for tag in resource_tags:
        if tag[key] == cli_tags()[0][key]:
            if tag[value] == cli_tags()[0][value]:
                return  True


    return False
def do_quit():
    """Exit the CLI."""
    quit("\nThank you for using Tomer AWS resource manager!")
