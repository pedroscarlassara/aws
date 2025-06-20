import boto3
from botocore.exceptions import NoCredentialsError, ParamValidationError
import requests

session = boto3.Session(
    profile_name = 'PROFILE_NAME_HERE',
    region_name = 'REGION_NAME_HERE'
)

client = session.client('s3')

def check_internet_connection():
    response = requests.get('https://checkip.amazonaws.com/')
    if response.status_code == 200:
        return True
    else:
        return False

def main():
    if check_internet_connection():
        print('1. List Bucket          2. Create Bucket            3. Delete Bucket')
        option = int(input())
        if option == 1:
            print(client.list_buckets()['Buckets'])
        elif option == 2:
            bucket_name = input('Name your bucket: ')
            bucket_region = input('Which region do you want to create the bucket: ')
            response = client.create_bucket(
                Bucket= f'{bucket_name}',
                #Check the avaiable regions at: https://docs.aws.amazon.com/AmazonS3/latest/API/API_CreateBucketConfiguration.html
                CreateBucketConfiguration={
                    'LocationConstraint': f'{bucket_region}',
                },
            )
            print(response)
        else:
            bucket_name = str(input('Bucket Name: '))
            try:
                client.delete_bucket(Bucket=str(bucket_name))
            except ParamValidationError as error:
                print(f'ParamValidationError: {error}')

print(main())
