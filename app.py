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

def upload_all_files(local_directory: str, destination: str, bucket: str):
    for root, dirs, files in os.walk(local_directory):
        for filename in files:
            with open(os.path.join(root, filename), 'rb') as f:
                s3.put_object(Bucket=bucket ,Body=f, Key=f'{destination}/{filename}')

def generate_permenant_link(path: str, bucket_name: str, monthes = 6):
    return s3.generate_presigned_url(
        "get_object",
        Params={"Bucket": bucket_name, "Key": path},
        ExpiresIn=monthes * 30 * 24 * 60 * 60,
    )

def list_all_objects(bucket: str):
    list = []
    files = s3.list_objects(Bucket=bucket)
    for file in files["Contents"]:
        list.append(file["Key"])