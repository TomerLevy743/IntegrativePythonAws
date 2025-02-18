import time
import boto3
import keyboard
import win_unicode_console



def do_login():
    """Login menu"""

    login_message = """
     Welcome to AWS Resource Manager 
    ==========================================

     Please enter your name to continue:

   

    (Press [Enter] when done...)

    ==========================================
        """
    print( login_message)
    name=input(  " name > " )
    if name == "admin":
         if not input("password: ") == "0000":
                exit()


    return name

def do_intro_screen():
    intro = """
    ==========================================
     AWS Resource Manager v1.0 
    ==========================================
    Manage your AWS resources with ease!

    🛠  Controls:
      [L] - List all active AWS resources
      [C] - Create a new resource
      [U] - Update an existing resource
      [D] - Delete a resource
      [S] - Check resource status
      [Q] - Quit program

     Connected to: [AWS Account: ****-****-****]
     Syncing with AWS...  {}

     Press a key to continue...
        """
    aws_credentials_not_found = "please configure your aws credentials before proceeding"
    sync_success= "✅"
    sync_result= sync_success
    sync_failed= "❌"
    # #check for aws credentials
    # sts = boto3.client('sts')
    # try:
    #     sts.get_caller_identity()
    #     sync_result = sync_success
    # except :
    #     sync_result = sync_failed
    #     print( aws_credentials_not_found )


    print(intro.format(sync_result))
    while True:
        if keyboard.is_pressed("a"):
            print("works")
            time.sleep(1)

def do_quit(self, line):
    """Exit the CLI."""
    print()
    exit()



if __name__ == '__main__':
    user_name = do_login()
    do_intro_screen()
    #
