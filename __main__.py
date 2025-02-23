import time
import botocore
import boto3
import keyboard
import manage_ec2
import manage_route53
import manage_s3
import utilities

def do_login():
    """Login menu"""
    utilities.clear_terminal()
    login_message = """
==================================================
        Welcome to AWS Resource Manager v1.0 
==================================================

         Please enter your name to continue:

         (Press [Enter] when done...)

==================================================
        """
    print(login_message)
    name=input(  " name > " )


    if name == "admin":
         if not input('Enter Password>') == "0000":
                 exit()

    return name


def do_intro_screen():
    intro = """
==================================================
        AWS Resource Manager v1.0 
==================================================
         Manage your AWS resources with ease!

         Connected to: [AWS Account: ****-****-****]
         Syncing with AWS...  {}

==================================================
"""

    utilities.clear_terminal()
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
    time.sleep(2)

def do_input_manager(user_id):
    controls_message = """
==================================================
        AWS Resource Manager v1.0 
==================================================
         Choose which resource you want to manage:
        [1] - EC2 
        [2] - S3
        [3] - Route 53
        [Q] - Quit program
      
Press a key to continue...
==================================================
"""
    utilities.clear_terminal()
    print(controls_message)
    while 1:
        if keyboard.is_pressed('1'):  # ec2
            manage_ec2.manager(user_id)
            return
        elif keyboard.is_pressed('2'):  # s3
            manage_s3.manager(user_id)
            return
        elif keyboard.is_pressed('3'):  # route53
            manage_route53.manager(user_id)
            return
        elif keyboard.is_pressed('q'):
            utilities.do_quit()





if __name__ == '__main__':
    user_id = do_login()
    do_intro_screen()
    do_input_manager(user_id)
    print("""
    
==================================================
         Thank You for Using Tomer Resource Manager!  
==================================================

        - Your session has ended.  
        - We hope the resources were helpful.  
        - If you need further assistance, don't hesitate to reach out.  

        - Have a great day and happy cloud managing!  

==================================================
""")
