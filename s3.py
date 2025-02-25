import time
import boto3
import json
import keyboard
from pyasn1.type.useful import ObjectDescriptor

import utilities

bucket_prefix = "tomer-cli-"

def get_buckets(client):

    response = client.list_buckets(
            MaxBuckets=123,
            Prefix=bucket_prefix,
            BucketRegion='us-east-1',
    )
    tagged_buckets= []
    for bucket in response['Buckets']:
        tags =  client.get_bucket_tagging(Bucket=bucket['Name'])['TagSet']
        # print(tags)

        if utilities.filter_by_tags(tags):
            temp = {'Name':bucket["Name"],'Prefix':response["Prefix"]}
            tagged_buckets.append(temp)

    return tagged_buckets


def bucket_message(bucket, prefix=""):
    return f"       {prefix}Prefix = {bucket['Prefix']} , Name = {bucket["Name"]} \n"


def list_cli_buckets(client):
    buckets = get_buckets(client)
    header ="S3 Bucket list"
    body = "\n"

    for bucket in buckets:
       body += bucket_message(bucket)

    body += "(Press [Enter] To Continue...)"
    utilities.print_and_confirm(header,body)



def get_access_level(header):

    info_message = """
        choose an Instance type:
        [1] - Private
        [2] - Public    
        """
    confirmation_message = """
        the bucket will be accessible by anyone. are you sure ?
        [Y] - Yes
        [N] - No
    """
    utilities.message_template(header,info_message)

    while 1:
        if keyboard.is_pressed('1'): #
            time.sleep(1)
            return "private"

        elif keyboard.is_pressed('2'): #
            time.sleep(1)
            utilities.message_template(header,confirmation_message)
            while 1:
                if keyboard.is_pressed('y'):

                    return 'public-read-write'
                elif keyboard.is_pressed('n'):
                    utilities.message_template(header,info_message)
                    break

        elif keyboard.is_pressed('b'):
                return -1


def change_bucket_access_level(client, bucket_name, access_level):
    flag = False
    if access_level == 'private':
        flag = True

    # print(bucket_name)
    response = client.put_public_access_block(
            Bucket= bucket_name,
            PublicAccessBlockConfiguration={
                'BlockPublicAcls': flag,
                'IgnorePublicAcls': flag,
                'BlockPublicPolicy': flag,
                'RestrictPublicBuckets': flag
            },
    )
    if not flag :
        bucket_policy = {
                    "Version": "2012-10-17",
                    "Statement": [
                    {
                        "Sid": "Statement",
                        "Effect": "Allow",
                        "Principal": "*",
                       	"Action": [
        			    	"s3:GetObject"
		            	],
                        "Resource": f"arn:aws:s3:::{bucket_name}/*"
                    }
                ]
            }

    # Convert the policy to JSON
        policy_json = json.dumps(bucket_policy)

        client.put_bucket_policy(Bucket=bucket_name,Policy=policy_json)


def add_tags_to_bucket(client, bucket):
    client.put_bucket_tagging(Bucket=bucket,
                              Tagging= {'TagSet':utilities.cli_tags()} )


def create_bucket(client):
    """ Create a S3 bucket """
    header ="        Creating AWS S3 Bucket... "
    utilities.message_template(header)
    bucket_name = bucket_prefix + input("\nChoose a name for your bucket > ")

    access_level = get_access_level(header)
    if access_level == -1:
        return
    body = f"""- Bucket Name: {bucket_name}  
        - Region: us-east-1  
        - Access level: {access_level} 
        - Status: Initializing... 

         Allocating resources...  
         Connecting to AWS...  
         Creating bucket...  

         Bucket creation in progress!  
         Check AWS Console for status updates.

    """
    utilities.message_template(header,body)
    response = client.create_bucket(Bucket=bucket_name)
    # change the bucket to public if necessary
    change_bucket_access_level(client, bucket_name, access_level)
    # adding tags to the bucket
    add_tags_to_bucket(client,bucket_name)

    header = "        AWS S3 Bucket Created Successfully!"
    body = f"""- Bucket Name: {bucket_name}  
        - Region: us-east-1  
        - Status: Completed  

         Resources allocated successfully.  
         Bucket is ready for use!  
         You can now upload, download, and manage files.  

         Check AWS Console for more details.
         
(Press [Enter] To Continue...)
    """
    utilities.print_and_confirm(header,body)

def manage_bucket(client,func):
    bucket = utilities.pick_resource(get_buckets(client), bucket_message)
    if bucket == -1:
        return

    utilities.flush_input()
    func(client,bucket)

def upload_file(client,bucket,file_path="",file_name=""):
    """ upload a file to s3"""
    if file_path == "" and file_name == "":
        file_path = input("Enter the path file you want to upload > ")
        file_name = input("Enter the name you want the file to have > ")

    response = client.upload_file(Filename=file_path,Bucket=bucket['Name'],Key=file_name)
    header = "        AWS S3 File Upload Successful!"
    body = f"""- Bucket Name: {bucket['Name']}   
        - Local File Path: {file_path}  
        - S3 File Name: {file_name}  
        - Region: us-east-1  
        - Status: Upload Completed  

         The file located at '{file_path}' has been successfully uploaded  
         to S3 under the name '{file_name}'.  


         Verify the upload in the AWS Console if needed.

(Press [Enter] To Continue...)"""
    utilities.print_and_confirm(header,body)


def delete_file(client,bucket,file_name = ""):
    """ terminate a file from s3 bucket"""
    if file_name == "":
        file_name = input("Enter the name of the file to delete")
    header = "        AWS S3 File Deletion Completed!"
    body = f"""- Bucket Name: {bucket['Name']} 
        - File Name: {file_name}  
        - Region: us-east-1  
        - Status: File Deleted   

         The specified file has been successfully removed.  
         No further action is required.  

         Verify file removal in the AWS Console if needed.
(Press [Enter] To Continue...)"""
    response = client.delete_object(Bucket=bucket['Name'],Key=file_name)
    utilities.print_and_confirm(header,body)


def delete_bucket(client,bucket):
    """ terminate a s3 bucket"""
    header = "        Deleting AWS S3 Bucket... Please Wait"
    body = """- Bucket Name: {0}  
        - Region: us-east-1  
        - Status: {1}.  

         {2}"""
    status_str = "Deletion Initiated.."
    progress_str = """Connecting to AWS...  
         Verifying bucket existence...  
         Removing all objects from bucket...  
         Deleting bucket...  

         Bucket deletion in progress!  
         Check AWS Console for status updates."""

    utilities.message_template(header,body.format(bucket['Name'],status_str,progress_str))

    response = client.delete_bucket(Bucket=bucket['Name'])
    header ="        AWS S3 Bucket Deleted Successfully!"
    status_str = "Deletion Completed"
    progress_str = """All objects removed successfully.  
         Bucket has been deleted from your AWS account.  

         Verify deletion in the AWS Console for confirmation.
         (Press [Enter] To Continue...)
    """
    utilities.message_template(header,body.format(bucket['Name'],status_str,progress_str))
    utilities.wait_for_enter()




def manager(user_id):
    utilities.clear_terminal()
    client = boto3.client('s3', 'us-east-1')
    time.sleep(1)
    header = "        S3 Manager v1.0"
    body = """
         Select:
        [C] - Create bucket
        [U] - Upload file"""

    if user_id == "admin":
        body += """
        [D] - Delete bucket
        [R] - Remove file"""


    body += """
        [L] - List all buckets
        [B] - Back to previous menu
        [Q] - Quit program

Press a key to continue...
             """

    utilities.message_template(header,body)
    while 1:
        if keyboard.is_pressed('c'):

            create_bucket(client)
            break
        elif keyboard.is_pressed('u'):
            manage_bucket(client,upload_file)
            break
        elif keyboard.is_pressed('d') and user_id == "admin":
            manage_bucket(client,delete_bucket)
            break
        elif keyboard.is_pressed('r') and user_id == "admin":
            manage_bucket(client,delete_file)
            break
        elif keyboard.is_pressed('l'):
            list_cli_buckets(client)
            break
        elif keyboard.is_pressed('b'):
            time.sleep(1)
            return
        elif keyboard.is_pressed('q'):
           utilities.do_quit()

    time.sleep(1)
    manager(user_id)


# manager("admin")
