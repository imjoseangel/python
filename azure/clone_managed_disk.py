import os
import traceback

from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import DiskCreateOption

from msrestazure.azure_exceptions import CloudError

from haikunator import Haikunator


haikunator = Haikunator()

def get_credentials():
    subscription_id = os.environ['AZURE_SUBSCRIPTION_ID']
    credentials = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentials, subscription_id

def get_credentialsalt():
    subscription_altid = os.environ['AZURE_SUBSCRIPTION_ALTID']
    credentialsalt = ServicePrincipalCredentials(
        client_id=os.environ['AZURE_CLIENT_ID'],
        secret=os.environ['AZURE_CLIENT_SECRET'],
        tenant=os.environ['AZURE_TENANT_ID']
    )
    return credentialsalt, subscription_altid

get_credentials()
get_credentialsalt()

# Azure Datacenter
location = 'westeurope'

# Resource Group
group_name = 'ResourceGroup'

credentials, subscription_id = get_credentials()
resource_client = ResourceManagementClient(credentials, subscription_id)
compute_client = ComputeManagementClient(credentials, subscription_id)
network_client = NetworkManagementClient(credentials, subscription_id)

credentialsalt, subscription_altid = get_credentialsalt()
resource_clientalt = ResourceManagementClient(credentialsalt, subscription_altid)
compute_clientalt = ComputeManagementClient(credentialsalt, subscription_altid)
network_clientalt = NetworkManagementClient(credentialsalt, subscription_altid)


managed_disk = compute_client.disks.get(group_name, 'ManagedDisk_OsDisk_1_9b9ca65cc8be41689e22fd6134610f29')


async_creation = compute_clientalt.disks.create_or_update(
    'ResourceGroup2',
    'my_disk_name',
    {
        'location': 'westeurope',
        'creation_data': {
            'create_option': DiskCreateOption.copy,
            'source_resource_id': managed_disk.id
                        }
      }
)
disk_resource = async_creation.result()
