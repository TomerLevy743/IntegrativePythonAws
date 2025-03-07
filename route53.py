import ipaddress
import time
from datetime import datetime
import boto3
import keyboard
import utilities


def add_tags_to_zone(client, zone_id,tags):
    client.change_tags_for_resource(
            ResourceType='hostedzone',
            ResourceId=zone_id,
            AddTags=tags,
    )


def extract_id(zone_id):
    id_index = zone_id.find("/", 1)
    return zone_id[id_index + 1:]

def validate_domain():
    # Regular expression for validating domain names
    pattern = re.compile(
        r'^(?:[a-zA-Z0-9]'            # First character of the domain
        r'(?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+'  # Subdomain + hostname
        r'[a-zA-Z]{2,}$'              # Top-level domain (TLD)
    )

    while 1:
        domain =input("Enter a domain >")
        if pattern.match(domain):
            return domain
        else:
            print(f" '{domain}' is not a valid domain. please enter a valid domain")

def create_zones(client):
    utilities.flush_input()
    header = "        Creating Route 53 Hosted Zone..."

    utilities.message_template(header)
    zone_name = validate_domain()

    body = """
        - Status: Initializing Hosted Zone Creation  
        - Verifying domain configuration...  
        - Allocating Route 53 resources...  
        - Establishing DNS settings...  

         Please wait while AWS Route 53 sets up your hosted zone."""

    utilities.message_template(header,body)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    response = client.create_hosted_zone(Name=zone_name,CallerReference=current_time)
    # add tags to the zone
    zone_id = response["HostedZone"]["Id"]
    zone_change_info = response["ChangeInfo"]["Id"]

    #print output
    header ="        Route 53 Hosted Zone Created Successfully!"
    body = """- Status: Hosted Zone Creation Complete  
        - DNS configuration is now active.  
        - You can manage DNS records from the AWS Route 53 Console.  
        - Ensure to update your domain registrar with the new name servers.  

         Hosted zone is now ready for use.  
                
(Press [Enter] To Continue...)"""
    utilities.print_and_confirm(header,body)
    return extract_id(zone_id)


def get_zones(client):
    """list all relevant zones ( filter by tags )"""
    response = client.list_hosted_zones()
    tagged_zones = []
    for zone in response['HostedZones']:
        zone_id = extract_id(zone['Id'])
        tags = client.list_tags_for_resource(
                ResourceType='hostedzone'
                ,ResourceId=zone_id
        )
        tags = tags["ResourceTagSet"]["Tags"]
        if utilities.filter_by_tags(tags):
            temp = {'Id':zone_id,'Name':zone['Name']}
            tagged_zones.append(temp)


    return tagged_zones

def print_zone(zone,prefix=""):
    return f"       {prefix}Id = {zone['Id']} , Name = {zone['Name']}\n"

def pick_zone(client,header):
    body = "Fetching zones please wait..."
    utilities.message_template(header,body)
    zones = get_zones(client)
    zone = utilities.pick_resource(zones, print_zone)
    if zone == -1:
        print("Need to create a hosted zone first!")
        return zone
    utilities.flush_input()
    return zone

def delete_zones(client,zone):
    header = "           Deleting Hosted Zone... Please Wait"
    body = f"""- Hosted Zone ID: {zone['Id']}
        - Domain Name: {zone['Name']}
        - Status: {1}  

         {2}"""
    status_message = "Deletion in Progress...  "

    progress_message = """Verifying hosted zone ownership...  
         Initiating hosted zone deletion...  

         Hosted zone deletion in progress!  
         Check the AWS Route 53 Console for status updates."""
    body = body.format(status_message,progress_message)
    utilities.message_template(header,body)
    # delete function
    response = client.delete_hosted_zone(Id=zone['Id'])

    header_message = "        Hosted Zone Deletion Completed Successfully!"
    status_message = "Successfully Deleted"
    progress_message = """The hosted zone has been deleted from AWS Route 53.  
            Thank you for using the AWS Resource Manager!"""

    body += """         
(Press [Enter] To Continue...)
    """
    body = body.format(status_message,progress_message)
    utilities.print_and_confirm(header,body)

import re



def validate_ip():
    while 1:
        ip = input("Value > ")
        try:
            # Validate the IP address (IPv4 or IPv6)
            ip_obj = ipaddress.ip_address(ip)
            print(f"'{ip}' is a valid {ip_obj.version}-bit IP address.")
            return ip
        except ValueError:
            print(f" '{ip}' is not a valid IP address. enter a valid ip")
            return ip

def manage_dns_record(client, zone, record_action="CREATE", record_config =""):
    if record_config == "":
        name = input("\nName > ")
        record_config = {"Name": f"{name}.{zone['Name']}",
                         'Type': 'A', 'DNS': validate_ip()}

    # create a string from record action that will be used for message
    action_name = record_action[0] + record_action[1:-1].lower() + "ing"
    if record_action == "UPSERT":
            action_name = record_action[0] + record_action[1:].lower() + "ing"

    head_line = "Please Wait"
    status = "Processing..."
    header =f"        {action_name} DNS Record... {0}"
    body = f"""- Hosted Zone: {zone['Name']}  
        - Record Name: {record_config['Name']}  
        - Record Type: A (IPv4 Address)  
        - Action: {record_action}
        - Status: {0}"""

    utilities.message_template(header.format(head_line),body.format(status))


    response = client.change_resource_record_sets(
            HostedZoneId=zone['Id'],
            ChangeBatch={
                'Changes': [
                    {
                        'Action': record_action,
                        'ResourceRecordSet': {
                            'Name': record_config['Name'],
                            'TTL': 60,
                            'Type': record_config['Type'],
                            'ResourceRecords': [
                                {
                                    'Value': record_config['DNS'],
                                },
                            ],
                        }
                    }
                ]
            }
    )

    head_line = "Done"
    status = "Complete"
    body += """         
(Press [Enter] To Continue...)
    """
    utilities.print_and_confirm(header,body)


def manager(user_id):
    client = boto3.client("route53", 'us-east-1')
    header = "        Route53 Manager v1.0"
    body = """Select:
        [C] - Create DNS Zone
        [M] - Make DNS Record
        [U] - Update DNS Record (Upsert)
        [D] - Delete DNS Record"""
    if user_id == "admin":
        body += """
        [R] - Delete DNS zone"""

    body += """
        [B] - Back to previous menu
        [Q] - Quit program

Press a key to continue..."""

    utilities.message_template(header,body)
    while 1:
        if keyboard.is_pressed('c'):
            zone_id = create_zones(client)
            time.sleep(0.5)
            add_tags_to_zone(client,zone_id,utilities.cli_tags())
            break
        elif keyboard.is_pressed('m'):
            zone = pick_zone(client,header)
            if not zone == -1 :
                manage_dns_record(client, zone,'CREATE')
            break
        elif keyboard.is_pressed('u'):
            zone = pick_zone(client,header)
            if not zone == -1:
                manage_dns_record(client, zone,"UPSERT")
            break
        elif keyboard.is_pressed('d'):
            zone = pick_zone(client,header)
            if not zone == -1:
                manage_dns_record(client, zone,"DELETE")
            break
        elif keyboard.is_pressed('r') and user_id == "admin":
            zone = pick_zone(client,header)
            if not zone == -1:
                delete_zones(client,zone)
            break
        elif keyboard.is_pressed('b'):
            time.sleep(0.5)
            return True
        elif keyboard.is_pressed('q'):
            utilities.do_quit()

    time.sleep(0.5)
    manager(user_id)

# client = boto3.client("route53", 'us-east-1')
# manager("admin")
# get_zones(client)
# delete_zones(client)