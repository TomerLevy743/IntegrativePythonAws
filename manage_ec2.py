import time

import boto3
import keyboard

import config_importer
import utilities

state_running="running"
state_paused="paused"

def get_instances(client,state):
    owner_tag = "tomerlevy"
    by_tag = "Created_By_Tomer_CLI"
    response =client.describe_instances(
        Filters=[
            {'Name': 'tag:Owner','Values': [owner_tag]},
            {'Name': 'tag:by','Values': [by_tag]},
            {'Name': 'instance-state-name','Values': state}
        ]
    )
    instances =[]
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            instances.append(instance['InstanceId'])

    return instances



def get_instance_type(instance_config):
    info_message = """
         choose an Instance type:
        [1] - t3.nano
        [2] - t4g.nano    
        """
    print(info_message)
    while 1:
        if keyboard.is_pressed('1'): #
            instance_config["instance-type"] = "t3.nano"
            time.sleep(1)
            return instance_config
        if keyboard.is_pressed('2'): #
            instance_config["instance-type"] = "t4g.nano"
            time.sleep(1)
            return instance_config

def get_image_id(instance_config,):
    info_message = """
         choose an Image ID:
        [1] - Amazon linux
        [2] - Ubuntu    
           """
    print(info_message)

    instance_type = instance_config["instance-type"]
    index = instance_type.find('.')
    architecture = instance_type[:index]
    while 1:
        if keyboard.is_pressed('1'):  #
            instance_config["image-id"] = instance_config["amazon-"
                                                          + architecture]
            time.sleep(1)
            return instance_config
        if keyboard.is_pressed('2'):  #
            instance_config["image-id"] = instance_config["ubuntu-"
                                                          + architecture]
            time.sleep(1)
            return instance_config


def get_instance_config(ec2):


    file_path = "ec2_configuration"
    instance_config = {}
    instance_config = config_importer.import_data(instance_config,file_path)
    utilities.flush_input()
    instance_config['name'] = input("\nChoose a name for your instance > ")
    instance_config = get_instance_type(instance_config)
    instance_config = get_image_id(instance_config,)

    return instance_config

# todo: add function to request for input (AMI and instance type)
def create_instance():

    ec2 = boto3.resource('ec2', region_name='us-east-1')
    client = boto3.client('ec2', region_name='us-east-1')
    max_running = 2
    if len(get_instances(client, [state_running])) >= max_running:
        print("\nYou cant create more instances while"
              " we already have two running!")
        return

    instance_config = get_instance_config(ec2)
    print(f"""
==================================================
        Creating AWS EC2 Instance... Please Wait
==================================================

        - Instance Type: {instance_config['instance-type']}  
        - Region: us-east-1  
        - Status: Provisioning...  

         Allocating resources...  
         Connecting to AWS...  
         Launching instance...  

         Instance creation in progress!  
         Check AWS Console for status updates.

=================================================="""
          )
    response = ec2.create_instances(
            ImageId=instance_config["image-id"],
            MinCount=1,
            MaxCount=1,
            InstanceType=instance_config["instance-type"],
            KeyName=instance_config["key-name"],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {
                            'Key': 'Name',
                            'Value': instance_config["name"]
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
            NetworkInterfaces=[
                {
                    'AssociatePublicIpAddress': True,
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
    creation_complete= """
==================================================
        AWS EC2 Instance Created Successfully
==================================================

        - Instance ID: {0}  
        - Instance Type: {1}  
        - Key: {2}  
        - Status: Running  

         Instance is now active and ready for use.  
         Use SSH or AWS Console to connect.  

==================================================""".format(response[0]
            ,instance_config["instance-type"],instance_config["key-name"])
    print(creation_complete)
    return response[0]


def select_instance(instances):
    max_instances = 9
    count = 0
    for instance in instances:
        print("""
         [{0}] - {1}""".format(count,instance))
        count+=1
        if count > max_instances:
            break
    while 1:
        count = 0
        for instance in instances:
            if keyboard.is_pressed(str(count)):
                return instance
            count += 1


def start_instance():
    client = boto3.client('ec2', region_name='us-east-1')

    instance =select_instance(get_instances(client,[state_paused]))

    response = client.start_instances(
         InstanceIds=[instance]
     )
    print("{} started".format(instance))
def pause_instance():
    client = boto3.client('ec2', region_name='us-east-1')

    instance =select_instance(get_instances(client,[state_running]))

    response = client.stop_instances(
         InstanceIds=[instance]
    )
    print("{} paused".format(instance))
def terminated_instance():
    client = boto3.client('ec2', region_name='us-east-1')

    instance = select_instance(get_instances(client, [state_running
        ,state_paused]))
    response = client.terminate_instances(
         InstanceIds=[instance]
    )
    print("{} terminated".format(instance))


def list_instances():
    client = boto3.client('ec2', region_name='us-east-1')

    print(get_instances(client,[state_running,state_paused]))


def manager(user_id):
    time.sleep(1)
    controls_message = """
==================================================
        EC2 Manager v1.0 
==================================================
         Select:
        [C] - Create instance
         
        [S] - Start instance
        [P] - Pause instance"""
    end_control_message = """
        [L] - List all instances
        [B] - Back to previous menu
        [Q] - Quit program
      
Press a key to continue...
==================================================
         """

    if user_id == "admin":
        controls_message+= """
        [D] - Delete instance"""

    controls_message += end_control_message

    print(controls_message)
    while 1:
        if keyboard.is_pressed('c'):
            create_instance()
            time.sleep(1)
            return
        elif keyboard.is_pressed('s'):
            start_instance()
            time.sleep(1)
            return
        elif keyboard.is_pressed('p'):
            pause_instance()
            time.sleep(1)
            return
        elif keyboard.is_pressed('d') and user_id == "admin":
            terminated_instance()
            time.sleep(1)
            return
        elif keyboard.is_pressed('l'):
            list_instances()
            time.sleep(1)
            return
        elif keyboard.is_pressed('b'):
            time.sleep(1)
            return True
        elif keyboard.is_pressed('q'):
            quit("\nThank you for using Tomer AWS resource manager!")


