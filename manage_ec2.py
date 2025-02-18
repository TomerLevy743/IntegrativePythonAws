import boto3
import datetime
import config_importer


#todo: add function to request for input (AMI and instance type)
def create_instance(ec2):
    file_path = ""
    dict_list = {}
    instance_config = config_importer.import_data(dict_list,file_path)

    n = 8  # create an instance with older date tag
    f_user_data = open(r"user_data.sh","r")
    user_data = f_user_data.read()
    date_tag = str(datetime.date.today() - datetime.timedelta(days=n)) # for testing
    response = ec2.create_instances(
        ImageId = instance_config["image-id"],
        MinCount=1,
        MaxCount=1,
        InstanceType = instance_config["instance-type"],
        KeyName =instance_config["key-name"],
        UserData = user_data,
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'Date',
                        'Value': date_tag
                    },
                    {
                        'Key': 'Owner',
                        'Value': 'tomerlevy'
                    },
                    {
                        'Key': 'by',
                        'Value': 'Created_By_tomer_CLI'
                    }
                ]
            },
        ],
        NetworkInterfaces = [
            {
            'AssociatePublicIpAddress': True ,
            'DeleteOnTermination': True,
            'Description': 'string',
            'DeviceIndex': 0,
            'SubnetId': 'subnet-032dba4d76776a812',
            'Groups': [
                instance_config["security-group"],
               ],

            },
        ],
    )
    print(response[0].private_ip_address)
    f_user_data.close()
    return response[0]


def get_instances(client):
    instance_tags =client.describe_instances(
        Filters=[
            {
                'Name': 'tag:Owner',
                'Values': [
                    'tomerlevy'
                ]
            }
        ]
    )
    instances= []
    # todo: add counter for running instances
    count = 0
    for reservation in instance_tags['Reservations']:
        for instance in reservation['Instances']:
            for tag in instance["Tags"]:
                if "Key" in tag and tag["by"] == "Created_By_tomer_CLI":
                        instances.append(instance)
    return instances
#todo: change into a start pause function
def delete_instances(client,instances):
    ids = []
    running = 16

    for instance_id in instances:
        if ("State" in instance_id
                and instance_id["State"]["Code"] == running):
            ids.append(instance_id["InstanceId"])

    if len(ids) == 0:
        return "no instance to delete"
    response = client.terminate_instances(
         InstanceIds=ids
     )
    return ids