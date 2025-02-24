import time

import boto3
import keyboard

import config_importer
import utilities

#todo: add logs for errors
state_running="running"
state_paused="paused"


def ec2_cli_tags():
    tags = utilities.cli_tags()
    key = utilities.get_key()
    value = utilities.get_value()
    return [
        {
            'Name': f'tag:{tags[0][key]}',
            'Values': [
                tags[0][value]
            ]
        },
        {
            'Name': f'tag:{tags[1][key]}',
            'Values': [
                tags[1][value]
            ]
        }

    ]
def get_instances(client,state):
    tags = ec2_cli_tags()
    tags.append({'Name': 'instance-state-name','Values':state})
    response =client.describe_instances(
        Filters=tags
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

def create_instance():

    ec2 = boto3.resource('ec2', region_name='us-east-1')

    instance_config = get_instance_config(ec2)
    tags = utilities.cli_tags()
    tags.append({'Key': 'Name','Value': instance_config["name"]})
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
                    'Tags': tags
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
    creation_complete= f"""
==================================================
        AWS EC2 Instance Created Successfully
==================================================

        - Instance ID: {response[0]}  
        - Instance Type: {instance_config["instance-type"]}  
        - Key: {instance_config["key-name"]}  
        - Status: Running  

         Instance is now active and ready for use.  
         Use SSH or AWS Console to connect.  

=================================================="""
    print(creation_complete)
    return response[0]


def manage_instance(client, action):

    actions = {
        'terminate':{
            "func": client.terminate_instances,
            'states': [state_paused, state_running],
            "message": "{} terminated"
        },
        'pause':{
        "func": client.stop_instances,
            "states":[ state_paused],
            "message": "{} paused"
        },
        'start':{
        "func": client.start_instances,
            "states":[state_running],
            "message": "{} started"
        }
    }

    instance = utilities.pick_resource(get_instances(client,actions[action]["states"]))
    response = actions[action]["func"](InstanceIds=[instance])
    print(actions[action]["message"].format(instance))


def list_instances(client):
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
    max_instances_message = ("\nYou cant create more instances while "
                             "we already have two running!")
    client = boto3.client('ec2', region_name='us-east-1')
    controls_message += end_control_message
    max_running = 2
    print(controls_message)
    while 1:
        if keyboard.is_pressed('c'):
            if len(get_instances(client, [state_running])) >= max_running:
                print(max_instances_message)
                continue

            create_instance()
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('s'):
            if len(get_instances(client, [state_running])) >= max_running:
                print(max_instances_message)
                continue

            manage_instance(client,"start")
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('p'):
            manage_instance(client, "pause")
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('d') and user_id == "admin":
            manage_instance(client, "terminate")
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('l'):
            list_instances(client)
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('b'):
            time.sleep(1)
            return True
        elif keyboard.is_pressed('q'):
            utilities.do_quit()


