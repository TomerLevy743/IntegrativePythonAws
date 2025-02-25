import os
import time

import keyboard


def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def flush_input():
    input(keyboard.press_and_release('enter'))

def pick_resource(resource_list, print_template):
        header = "      Pick a resource to operate on:"
        max_resources = 9
        count = 0
        body = "\n"
        if len(resource_list) == 0:
            return -1

        for resource in resource_list:
            prefix = f"[{count}] - "
            body +=print_template(resource, prefix)
            count += 1
            if max_resources > 9:
                break

        message_template(header,body)
        while 1:
            count = 0
            for resource in resource_list:
                if keyboard.is_pressed(str(count)):
                    return resource
                elif keyboard.is_pressed('b'):
                    return -1

                count += 1

def get_key():
    return "Key"
def get_value():
    return "Value"

def wait_for_enter():

    while 1:
        if keyboard.is_pressed('enter'):
            return

def cli_tags():
    return [
        {
            get_key(): 'by',
            get_value(): 'tomer-cli'
        },
        {
            get_key(): 'owner',
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
def get_template_line():
    return "=================================================="


def message_template(header, body="",flush=True):
    line = get_template_line()
    message = f"""
{line}
{header}
{line}"""
    if not body == "":
        message +=f"""
        {body}
{line}
"""
    if flush:
        flush_input()
    clear_terminal()
    time.sleep(1)
    print(message)

def print_and_confirm(header,body):
    message_template(header,body)
    wait_for_enter()

def do_quit():
    """Exit the CLI."""
    line = get_template_line()
    exit_message = f"""
{line}
         Thank You for Using Tomer Resource Manager!  
{line}

        - Your session has ended.  
        - We hope the resources were helpful.  
        
        - If you need further assistance, don't hesitate to reach out.  

        - Have a great day and happy cloud managing!  

{line}
"""
    quit(exit_message)
