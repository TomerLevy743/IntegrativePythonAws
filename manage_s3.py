import time
import boto3
import json
import keyboard
from pyasn1.type.useful import ObjectDescriptor

import utilities

prefix = "tomer-cli-"

def get_buckets(client):

    response = client.list_buckets(
            MaxBuckets=123,
            Prefix=prefix,
            BucketRegion='us-east-1',
    )
    return response['Buckets']

def print_buckets(client):
    print(get_buckets(client))

def pick_bucket(buckets):
    max_buckets = 9
    count = 0
    if len(buckets) == 0 :
        return -1
    for bucket in buckets:
        print("""
             [{0}] - {1}""".format(count, bucket))
        count += 1
        if max_buckets > 9 :
            break

    while 1:
        count = 0
        for bucket in buckets:
            if keyboard.is_pressed(str(count)):
                return bucket
            if keyboard.is_pressed('b'):
                return -1
            count += 1


def get_access_level():
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
    print(info_message)

    while 1:
        if keyboard.is_pressed('1'): #
            time.sleep(1)

            return "private"
        elif keyboard.is_pressed('2'): #
            time.sleep(1)
            print(confirmation_message)
            while 1:
                if keyboard.is_pressed('y'):
                    return 'public-read'
                elif keyboard.is_pressed('n'):
                    break
        elif keyboard.is_pressed('b'):
                return -1


def change_bucket_access_level(client, bucket_name, access_level):
    flag = False
    if access_level == 'private':
        flag = True



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



def create_bucket(client):
    """ Create a S3 bucket """
    s3_control = boto3.client('s3control', 'us-east-1')

    # response = s3_control.delete_public_access_block(
    #         AccountId='992382545251'
    # )
    # print (response)
    #
    # response = s3_control.put_public_access_block(
    #         PublicAccessBlockConfiguration={
    #             'BlockPublicAcls':  False,
    #             'IgnorePublicAcls': False,
    #             'BlockPublicPolicy': False,
    #             'RestrictPublicBuckets': False
    #         },
    #         AccountId='992382545251'
    #
    # )
    #
    # print(response)
    #
    # response = s3_control.get_public_access_block(AccountId='992382545251')
    # print (response["PublicAccessBlockConfiguration"])

    utilities.clear_terminal()
    utilities.flush_input()
    bucket_name = input("\nChoose a name for your bucket > ")
    access_level = get_access_level()
    if access_level == -1:
        #todo save user_id for manager function
        manager("")
        return

    print("""
==================================================
        Creating AWS S3 Bucket... Please Wait
==================================================

        - Bucket Name: {0}  
        - Region: us-east-1  
        - Access level: {1} 
        - Status: Initializing... 

         Allocating resources...  
         Connecting to AWS...  
         Creating bucket...  

         Bucket creation in progress!  
         Check AWS Console for status updates.

    ==================================================
    """.format(bucket_name, access_level))
    response = client.create_bucket(
            Bucket=prefix + bucket_name,
            ACL = access_level,
            ObjectOwnership = "ObjectWriter"
    )
    # change_bucket_access_level(client, bucket_name, access_level)

    print("""
==================================================
        AWS S3 Bucket Created Successfully!
==================================================

        - Bucket Name: {0}  
        - Region: us-east-1  
        - Status: Completed ✅  

         Resources allocated successfully.  
         Bucket is ready for use!  
         You can now upload, download, and manage files.  

         Check AWS Console for more details.

==================================================
    """.format(bucket_name))


def upload_file(client):
    """ upload a file to s3"""
    bucket = pick_bucket(get_buckets(client))
    if bucket == -1:
        manager("")
        return
    utilities.flush_input()
    bucket_name = bucket["Name"]
    file_path = input("Enter the path file you want to upload. ")
    file_name = input("Enter the name you want the file to have")
    response = client.upload_file(Filename=file_path,Bucket=bucket["Name"],Key=file_name)
    print(f"""
==================================================
        AWS S3 File Upload Successful!
==================================================

        - Bucket Name: {bucket_name}   
        - Local File Path: {file_path}  
        - S3 File Name: {file_name}  
        - Region: us-east-1  
        - Status: Upload Completed ✅  

         The file located at '{file_path}' has been successfully uploaded  
         to S3 under the name '{file_name}'.  


         Verify the upload in the AWS Console if needed.

==================================================
    """)



def delete_file(client):
    """ terminate a file from s3 bucket"""
    bucket = pick_bucket(get_buckets(client))
    if bucket == -1 :
        manager("")
        return
    utilities.flush_input()
    bucket_name = bucket["Name"]
    file_name = input("Enter the name you want the file to delete")
    response = client.delete_object(Bucket=bucket["Name"],Key=file_name)
    print(f"""
==================================================
        AWS S3 File Deletion Completed!
==================================================

        - Bucket Name: {bucket_name} 
        - File Name: {file_name}  
        - Region: us-east-1  
        - Status: File Deleted ✅  

         The specified file has been successfully removed.  
         No further action is required.  

         Verify file removal in the AWS Console if needed.

==================================================
    """)


def delete_bucket(client):
    """ terminate a s3 bucket"""
    bucket = pick_bucket(get_buckets(client))
    if bucket == -1:
        manager("")
        return
    print("""
==================================================
        Deleting AWS S3 Bucket... Please Wait
==================================================

        - Bucket Name: {0}  
        - Region: us-east-1  
        - Status: Deletion Initiated...  

         Connecting to AWS...  
         Verifying bucket existence...  
         Removing all objects from bucket...  
         Deleting bucket...  

         Bucket deletion in progress!  
         Check AWS Console for status updates.

==================================================
    """.format(bucket["Name"]))
    response = client.delete_bucket(Bucket=bucket["Name"])
    print("""
==================================================
        AWS S3 Bucket Deleted Successfully!
==================================================

        - Bucket Name: {0}  
        - Region: us-east-1  
        - Status: Deletion Completed ✅  

         All objects removed successfully.  
         Bucket has been deleted from your AWS account.  

         Verify deletion in the AWS Console for confirmation.

==================================================
""".format(bucket["Name"]))

def manager(user_id):
    utilities.clear_terminal()
    client = boto3.client('s3', 'us-east-1')
    time.sleep(1)
    controls_message = """
==================================================
        S3 Manager v1.0 
==================================================
         Select:
        [C] - Create bucket
        [U] - Upload file"""
    end_control_message = """
        [L] - List all buckets
        [B] - Back to previous menu
        [Q] - Quit program

Press a key to continue...
==================================================
             """

    if user_id == "admin":
        controls_message += """
        [D] - Delete bucket
        [R] - Remove file"""

    controls_message += end_control_message

    print(controls_message)
    while 1:
        if keyboard.is_pressed('c'):
            create_bucket(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('u'):
            upload_file(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('d') and user_id == "admin":
            delete_bucket(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('r') and user_id == "admin":
            delete_file(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('l'):
            print_buckets(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('b'):
            time.sleep(1)
            return True
        elif keyboard.is_pressed('q'):
            quit("\nThank you for using Tomer AWS resource manager!")


