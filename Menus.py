import botocore
import boto3
import keyboard

import manage_ec2
import manage_route53
import manage_s3


def do_login():
    """Login menu"""

    login_message = """
    ==========================================
     Welcome to AWS Resource Manager 
    ==========================================

     Please enter your name to continue:

   

    (Press [Enter] when done...)

    ==========================================
        """
    name=input(  " name > " )


    if name == "admin":
         if not input('Enter Password>') == "0000":
                 exit()

    return name


def do_intro_screen():
    intro = """
    ==========================================
     AWS Resource Manager v1.0 
    ==========================================
     Manage your AWS resources with ease!

     Connected to: [AWS Account: ****-****-****]
     Syncing with AWS...  {}

     
    """


    aws_credentials_not_found = "please configure your aws credentials before proceeding"
    sync_success= "success"
    sync_result = sync_success
    sync_failed= "failure"
    #check for aws credentials
    sts = boto3.client('sts')
    try:
        sts.get_caller_identity()
        sync_result = sync_success
    except botocore.exceptions.ClientError:
        sync_result = sync_failed
        exit(aws_credentials_not_found)

    print(intro.format(sync_result))


def do_input_manager(user_id):
    controls_message = """
    ==========================================
     AWS Resource Manager v1.0 
    ==========================================
     Choose which resource you want to manage:
      [1] - EC2 
      [2] - S3
      [3] - Route 53
      [Q] - Quit program
      
      Press a key to continue...
"""
    while 1:
        if keyboard.is_pressed('1'):  # ec2
            manage_ec2.manager(user_id)
            return
        elif keyboard.is_pressed('2'):  # s3
            manage_s3.manager(user_id)
        elif keyboard.is_pressed('3'):  # route53
            manage_route53.manager(user_id)
        elif keyboard.is_pressed('q'):
            do_quit()


def do_quit():
    """Exit the CLI."""
    exit()



if __name__ == '__main__':
    user_id = do_login()
    do_intro_screen()
    do_input_manager(user_id)
