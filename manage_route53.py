import boto3


def create_zones():
    client = boto3.client("Route53",'us-east-1')
    response = client.create_hosted_zone(
            Name='string',
            VPC={
                'VPCRegion': 'us-east-1',
                'VPCId': 'string'
            },
            CallerReference='string',
            HostedZoneConfig={
                'Comment': 'string',
                'PrivateZone': True | False
            },
            DelegationSetId='string'
    )
#todo: admin only
def delete_zones():
    pass

def update_dns_records():
    pass
def create_dns_records():
    pass
def delete_dns_records():
    pass


def manager(user_id):
    return None
