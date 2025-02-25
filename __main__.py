import time
import botocore
import boto3
import keyboard
import ec2
import route53
import s3
import utilities

def do_login():
    """Login menu"""
    header ="        Welcome to AWS Resource Manager v1.0"
    body = """Please enter your name to continue:

(Press [Enter] when done...)"""

    utilities.message_template(header,body,False)
    name=input(  " name > " )


    if name == "admin":
         if not input('Enter Password>') == "0000":
                 exit()

    return name


def do_intro_screen():
    header = "        AWS Resource Manager v1.0 "
    body = """Manage your AWS resources with ease!

         Connected to: [AWS Account: ****-****-****]
         Syncing with AWS...  {}"""


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

    body.format(sync_result)
    utilities.message_template(header,body)
    time.sleep(2)

def do_input_manager(user):
    header = "        AWS Resource Manager v1.0 "
    body = """Choose which resource you want to manage:
        [1] - EC2 
        [2] - S3
        [3] - Route 53
        [Q] - Quit program
      
Press a key to continue..."""

    utilities.message_template(header,body)

    while 1:
        if keyboard.is_pressed('1'):  # ec2
            ec2.manager(user)

            break
        elif keyboard.is_pressed('2'):  # s3
            s3.manager(user)
            break
        elif keyboard.is_pressed('3'):  # route53
            (route53
             .manager(user))
            break
        elif keyboard.is_pressed('q'):
            utilities.do_quit()
    do_input_manager(user)




if __name__ == '__main__':
    user_id = do_login()
    do_intro_screen()
    do_input_manager(user_id)
