import time
from datetime import datetime
import boto3
import keyboard
import utilities


cli_tags = [
                        {
                            'Key': 'by',
                            'Value': 'tomer-cli'
                        },
                        {
                            'Key': 'Owner',
                            'Value': 'tomerlevy'
                        }
]


def add_tags_to_zone(client, zone_id,tags):
    client.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=tags,
    )


def extract_id(zone_id):
    id_index = zone_id.find("/", 1)
    return zone_id[id_index + 1:]


def create_zones(client):
    utilities.flush_input()
    zone_name = input("\nChoose a name for your zone > ")
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
    now = datetime.now()

    current_time = now.strftime("%H:%M:%S")
    response = client.create_hosted_zone(Name=zone_name,CallerReference=current_time)
    # add tags to the zone
    zone_id = response["HostedZone"]["Id"]
    zone_change_info = response["ChangeInfo"]["Id"]

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
    print("print zone_id")
    print(zone_id)
    return extract_id(zone_id)

def filter_by_tags(client, zone_id):
    response = client.list_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id
    )
    key = "Key"
    value = "Value"
    tags = response["ResourceTagSet"]["Tags"]
    for tag in tags:

        if tag[key] == cli_tags[0][key]:
            if tag[value] == cli_tags[0][value]:
                return  True


    return False


def get_zones(client):
    """list all relevant zones ( filter by tags )"""
    response = client.list_hosted_zones()
    tagged_zones = []
    for zone in response['HostedZones']:
        zone_id = extract_id(zone['Id'])
        if filter_by_tags(client,zone_id):
            tagged_zones.append(zone_id)

    print(tagged_zones)
    return tagged_zones



def delete_zones(client):
    """TODO: delete zones for admin only"""
    zones = get_zones(client)
    zone_id = utilities.pick_resource(zones)
    response = client.delete_hosted_zone(Id=zone_id)


def get_domain_name(client, zone_id):
    response = client.get_hosted_zone(Id = zone_id)
    domain_name = response["HostedZone"]["Name"]
    return domain_name


def manage_dns_record(client, record_action="CREATE"):

    zones = get_zones(client)
    zone_id = utilities.pick_resource(zones)
    zone_name = get_domain_name(client,zone_id)
    utilities.flush_input()
    record_name = f"{input("\nName > ")}.{zone_name}"
    record_type = 'A'
    dns_value = input("Value > ")
    action_name = record_action[0] + record_action[1:-1].lower() + "ing"
    if record_action == "UPSERT":
        action_name = record_action[0] + record_action[1:].lower() + "ing"
    head_line = "Please Wait"
    status = "Processing..."
    manage_record_message = f"""
==================================================
        {action_name} DNS Record... {0}
==================================================
        - Hosted Zone: {zone_name}  
        - Record Name: {record_name}  
        - Record Type: A (IPv4 Address)  
        - Action: {record_action}
        - Status: {1}  
==================================================
    """

    print(manage_record_message.format(head_line,status))
    response = client.change_resource_record_sets(
            HostedZoneId=zone_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': record_action,
                        'ResourceRecordSet': {
                            'Name': record_name,
                            'TTL': 60,
                            'Type': record_type,
                            'ResourceRecords': [
                                {
                                    'Value': dns_value,
                                },
                            ],
                        }
                    }
                ]
            }
    )
    head_line = "Done"
    status = "Complete"

    print(manage_record_message.format(head_line, status))




def manager(user_id):
    time.sleep(1)
    client = boto3.client("route53", 'us-east-1')
    controls_message = """
==================================================
        Route53 Manager v1.0 
==================================================
         Select:
        [C] - Create DNS Zone
        [M] - Make DNS Record
        [U] - Update DNS Record (Upsert)
        [D] - Delete DNS Record"""
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
            zone_id = create_zones(client)
            time.sleep(1)
            add_tags_to_zone(client,zone_id,cli_tags)
            manager(user_id)
            return
        elif keyboard.is_pressed('M'):
            manage_dns_record(client,'CREATE')
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('u'):
            manage_dns_record(client,"UPSERT")
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('d'):
            manage_dns_record(client,"DELETE")
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('r') and user_id == "admin":
            delete_zones(client)
            time.sleep(1)
            manager(user_id)
            return
        elif keyboard.is_pressed('b'):
            time.sleep(1)
            return True
        elif keyboard.is_pressed('q'):
            utilities.do_quit()

client = boto3.client("route53", 'us-east-1')
manager("admin")
# get_zones(client)
# delete_zones(client)