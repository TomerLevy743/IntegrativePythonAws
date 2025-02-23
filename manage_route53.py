import boto3


def get_zone_name():
    """TODO: get the domain name from the user"""

    return ""


def create_zones(client):

    zone_name = get_zone_name()
    #TODO: add output for start
    response = client.create_hosted_zone(Name=zone_name,CallerReference='test',
    )
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
    #TODO: add output for completion

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
    return 0


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
    client = boto3.client("Route53", 'us-east-1')
    #todo: add manager
    return None
