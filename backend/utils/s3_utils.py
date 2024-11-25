import boto3
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_obj, key):
    s3.upload_fileobj(file_obj, BUCKET_NAME, key)
    return f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
