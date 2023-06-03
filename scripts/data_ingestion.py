import boto3
import gdown
import os
from dotenv import load_dotenv
load_dotenv()

ACCESS_KEY = os.getenv('ACCESS_KEY')
SECRET_KEY = os.getenv('SECRET_KEY')
REGION_NAME = os.getenv('REGION_NAME')
BUCKET = os.getenv('BUCKET')

# This data ingestion file: 1. downloads Google drive files into your local machine (computer)
# 2. and then finally uploads them into an AWS S3 bucket.
# Make sure to set your AWS credentials within your environment via the terminal.
# The easiest way is through the AWS cli using the command: aws configure


def drive_to_s3_download(drive_url):
    # Checks if the url provided is a legit Google drive url.
    # If not it will provide an error message.
    if "drive.google" not in drive_url:
        print(f'{drive_url} is not a valid Google drive url. Please try again.')
        return f'{drive_url} is not a valid Google drive url. Please try again.'

    # Initializes the s3 client using your AWS credential vairables set above
    s3_client = boto3.client(
        's3',
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        region_name=REGION_NAME,
    )

    # This will download all files within the folder specified in the Google drive url
    # (in our case: Data Ingestion) into a new folder created in your local machine called 'Data Ingestion'.
    gdown.download_folder(url=drive_url, quiet=False, use_cookies=False)

    # Not required, but I changed the name of the new folder made above so that it doesn't have
    # spaces and matches this variable created below.
    directory = 'Data_Ingestion'
    # This will start the process of uploading the files that were just recently downloaded from
    # your Google drive into the s3 bucket.
    # This will take a few minutes, but no more than 5ish.
    for file in os.listdir(os.path.abspath(directory)):
        # Absolute path of the directory variable above
        absolute_path = os.path.abspath(directory)
        # Destination S3 location name for the uploaded files
        destination_file_in_s3_bucket = f'{file}'
        # This is the local storage location path within your local machine
        from_local_storage = f'{absolute_path}/{file}'
        s3_client.upload_file(from_local_storage, BUCKET,
                              destination_file_in_s3_bucket)

    print('Looks like everything worked out!')


drive_to_s3_download(
    'https://drive.google.com/drive/u/0/folders/14qzgV_wmF_jU-JaguIICPityt1gR_W-S')
