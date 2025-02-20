import boto3

def create_s3():
    client = boto3.client('S3','us-east-1')
    #todo: s3 configure access and name (confirmation message for public bucket)
    #todo: output creating bucket
    response = client.create_bucket(
            ACL='private' | 'public-read' | 'public-read-write' | 'authenticated-read',
            Bucket='string')

    #todo: output bucket completion

#todo: select a bucket and upload a image
def upload_image():
    pass
#todo?: delete image for admin
def delete_image():
    pass
#todo: delete a bucket for admin
def delete_bucket():
    pass

#TODO: create CLI interface for s3
def manager(user_id):
    return None