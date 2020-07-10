import boto3
import os
from Setting import Settings

def upload_files(path):
    session = boto3.Session(
        aws_access_key_id = Settings.aws_access_key_id,
        aws_secret_access_key= Settings.aws_secret_access_key,
        region_name= Settings.region_name
    )
    s3 = session.resource('s3')
    bucket = s3.Bucket('openverse-lms')
 
    for subdir, dirs, files in os.walk(path):
        for file in files:
            full_path = os.path.join(subdir, file)
            with open(full_path, 'rb') as data:
                path = path.replace('/','')
                bucket.put_object(Key=full_path[len(path)+1:], Body=data)
 
def download_dir(dist = '', local='/tmp', bucket='your_bucket'):

    session = boto3.Session(
        aws_access_key_id = Settings.aws_access_key_id,
        aws_secret_access_key= Settings.aws_secret_access_key,
        region_name= Settings.region_name
    )
    
    client  = session.client('s3')
    resource = session.resource('s3')

    paginator = client.get_paginator('list_objects')
    for result in paginator.paginate(Bucket=bucket, Delimiter='/', Prefix=dist):
        if result.get('CommonPrefixes') is not None:
            for subdir in result.get('CommonPrefixes'):
                download_dir(client, resource, subdir.get('Prefix'), local, bucket)
        for file in result.get('Contents', []):
            dest_pathname = os.path.join(local, file.get('Key'))
            if not os.path.exists(os.path.dirname(dest_pathname)):
                os.makedirs(os.path.dirname(dest_pathname))
            resource.meta.client.download_file(bucket, file.get('Key'), dest_pathname)

if __name__ == "__main__":
    
    pass
    # upload_files('ProjectsForTeacher/')
    # download_dir(local='ProjectsForStudent', bucket=Settings.bucketName)