import time
from fileinput import close

import boto3
import keyboard


def get_zone_name():
    """TODO: get the domain name from the user"""
    return  input("\nChoose a name for your zone > ")




def create_zones(client):
    zone_name = get_zone_name()
    #print create start
    print("""
==================================================
        Creating Route 53 Hosted Zone... Please Wait
==================================================

        - Status: Initializing Hosted Zone Creation  
        - Verifying domain configuration...  
        - Allocating Route 53 resources...  
        - Establishing DNS settings...  

         Please wait while AWS Route 53 sets up your hosted zone.

==================================================
    """)
    response = client.create_hosted_zone(Name=zone_name,CallerReference='test')
    # add tags to the zone
    zone_id = response["HostedZone"]["Id"]
    client.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=[
                {
                    'Key': 'by',
                    'Value': 'tomer-cli'
                },
                {
                    'Key': 'Owner',
                    'Value': 'tomerlevy'
                }
            ],

    )
    #print output
    print("""
==================================================
        Route 53 Hosted Zone Created Successfully!
==================================================

        - Status: Hosted Zone Creation Complete ✅  
        - DNS configuration is now active.  
        - You can manage DNS records from the AWS Route 53 Console.  
        - Ensure to update your domain registrar with the new name servers.  

         Hosted zone is now ready for use.

==================================================
    """)

def select_zone(zones):
    """select a specific zone from list"""
    return 0


def get_zones(client):
    """list all relevant zones ( filter by tags )"""
    response = client.list_hosted_zones(
            Marker='string',
            MaxItems='string',
            DelegationSetId='string',
            HostedZoneType='PrivateHostedZone'
    )
    tagged_zones = []
    # for reservation in response['Reservations']:
    #     for instance in reservation['Instances']:
    #         instances.append(instance['InstanceId'])


def delete_zones(client):
    """TODO: delete zones for admin only remove dns record if needed"""
    zones = get_zones(client)
    zone_name = select_zone(zones)
    response = client.delete_hosted_zone(
            Id=zone_name
    )

def manage_dns_record(client, record_action=None):
    zone_name = ""
    dns_name = ""
    collection_id = ""
    location_name = ""
    record_action = "create" # 'CREATE'|'DELETE'|'UPSERT'
    record_name = ""
    record_type = ""
    response = client.change_resource_record_sets(
            HostedZoneId=zone_name,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': record_action,
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'Type': record_type,

                            'AliasTarget': {
                                'HostedZoneId': zone_name,
                                'DNSName': dns_name,
                                'EvaluateTargetHealth': False
                            }
                        }
                    }
                ]
            }
    )


def manager(user_id):
    time.sleep(1)
    client = boto3.client("Route53", 'us-east-1')
    controls_message = """
==================================================
        Route53 Manager v1.0 
==================================================
         Select:
        [C] - Create DNS zone
        [S] - Create DNS records
        [M] - Manage DNS records
        [D] - Delete DNS records"""
    end_control_message = """
        [B] - Back to previous menu
        [Q] - Quit program

Press a key to continue...
==================================================
             """

    if user_id == "admin":
        controls_message += """
        [R] - Delete DNS zone"""

    controls_message += end_control_message

    print(controls_message)
    while 1:
        if keyboard.is_pressed('c'):
            create_zones(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('s'):
            manage_dns_record(client,'create')
            time.sleep(1)
            return
        elif keyboard.is_pressed('m'):
            manage_dns_record(client,"manage")
            time.sleep(1)
            return
        elif keyboard.is_pressed('d'):
            manage_dns_record(client,"delete")
            time.sleep(1)
            return
        elif keyboard.is_pressed('r') and user_id == "admin":
            delete_zones(client)
            time.sleep(1)
            return
        elif keyboard.is_pressed('b'):
            time.sleep(1)
            return True
        elif keyboard.is_pressed('q'):
            quit("\nThank you for using Tomer AWS resource manager!")


