import boto3
session = boto3.Session(profile_name="default")
import re
from botocore.exceptions import ClientError

ec2 = boto3.resource('ec2', region_name='eu-west-1')
volumes = ec2.volumes.all() # If you want to list out all volumes
volumes = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available']}])
volume_ids = []
for volume in volumes:
	volume_ids.append(volume.id)
ec2_client = boto3.client('ec2', region_name='eu-west-1')
unused_volume_snapshots = ec2_client.describe_snapshots(OwnerIds=['self'], Filters=[{'Name' : 'volume-id', 'Values': volume_ids}])['Snapshots']
#unused_volume_snapshots list  will contain the list of all the snapshots that are currently linked to volumes that are not in use i,e those
#volumes which are in available state
print('Unused Volume Snapshots')
for snap in unused_volume_snapshots:
	print(snap['SnapshotId'])

#all_snapshots list will contain the list of all_the snapshots in eu-west-1 region

all_snapshots = ec2_client.describe_snapshots(OwnerIds=['self'])['Snapshots']
print("All snapshots")
for snap in all_snapshots:
	print(snap['SnapshotId'])

#To filter Snapshots Created as a Part of create Image Api call.
create_image_snapshots = []
for snap in all_snapshots:
	if re.match(r"^Created by CreateImage\((.*?)\) for (.*?)", snap['Description']):
		create_image_snapshots.append(snap)


#Below is the query for the list of all snapshots which are linked to volumes that are available and inuse
used_and_unused_volume_ids = []
volumes_available_and_in_use = ec2.volumes.filter(Filters=[{'Name': 'status', 'Values': ['available', 'in-use']}])
for volume in volumes_available_and_in_use:
	used_and_unused_volume_ids.append(volume.id)
used_and_unused_volume_snapshots = ec2_client.describe_snapshots(OwnerIds=['self'], Filters=[{'Name' : 'volume-id', 'Values': volume_ids}])['Snapshots']
print('Create Image Snapshots')
for snap in create_image_snapshots:
	print(snap['SnapshotId'])


# To get the list of snapshots that are linked to those volumes which are deleted we need to filter the snapshots from all Snapshots
#i,e deleted_snapshots = all_snapshots - (snapshots of used volumes + snapshots of unused volume)
deleted_volumes_snapshots = []

for snap in all_snapshots:
	if snap not in used_and_unused_volume_snapshots:
		deleted_volumes_snapshots.append(snap)
print("Deleted Volume Snapshots")
for snap in deleted_volumes_snapshots:
	print(snap['SnapshotId'])
#
for snap in unused_volume_snapshots: #for deleting the snapshots that are currently linked to unused volumes
	try:
		print("Deleting snapshot "+snap['SnapshotId'])
		ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
	except ClientError as e:
		print(snap["SnapshotId"]+" cannot be deleted because used by an AMI")
		continue

for snap in deleted_volumes_snapshots: #for deleting the snapshots that are currently linked to deleted volumes
	try:
		print("Deleting snapshot "+snap['SnapshotId'])
		ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
	except ClientError as e:
		print(snap["SnapshotId"]+" cannot be deleted because used by an AMI")
		continue

for snap in create_image_snapshots:
	try:
		print("Deleting snapshot "+snap['SnapshotId'])
		ec2_client.delete_snapshot(SnapshotId=snap['SnapshotId'])
	except ClientError as e:
		print(snap["SnapshotId"]+" cannot be deleted because used by an AMI")
		continue
