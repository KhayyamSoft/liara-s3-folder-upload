from dotenv import load_dotenv
import boto3
import os

load_dotenv()

LIARA_ENDPOINT = os.getenv("LIARA_ENDPOINT")
LIARA_ACCESS_KEY = os.getenv("LIARA_ACCESS_KEY")
LIARA_SECRET_KEY = os.getenv("LIARA_SECRET_KEY")
LIARA_BUCKET_NAME = os.getenv("LIARA_BUCKET_NAME")

s3 = boto3.client(
    "s3",
    endpoint_url=LIARA_ENDPOINT,
    aws_access_key_id=LIARA_ACCESS_KEY,
    aws_secret_access_key=LIARA_SECRET_KEY,
)

local_directory = "upload_folder"
destination = "remote_upload_folder"

for root, dirs, files in os.walk(local_directory):
    for filename in files:
        # construct the full local path
        local_path = os.path.join(root, filename)

        # construct the full Dropbox path
        relative_path = os.path.relpath(local_path, local_directory)
        s3_path = os.path.normpath(destination + "/" + filename + "/")

        with open(local_path, 'rb') as f:
            s3.put_object(Bucket=LIARA_BUCKET_NAME ,Body=f, Key=f'{destination}/{filename}')