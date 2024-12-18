import boto3
import os
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Log environment variables to ensure they're set
logging.debug("AWS_ACCESS_KEY_ID: %s", os.getenv("AWS_ACCESS_KEY_ID"))
logging.debug("AWS_SECRET_ACCESS_KEY: %s", os.getenv("AWS_SECRET_ACCESS_KEY"))
logging.debug("AWS_REGION: %s", os.getenv("AWS_REGION"))
logging.debug("S3_BUCKET_NAME: %s", os.getenv("S3_BUCKET_NAME"))

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_obj, key):
    try:
        logging.debug("Uploading file to S3 with key: %s", key)
        s3.upload_fileobj(file_obj, BUCKET_NAME, key)
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
        logging.debug("File uploaded successfully: %s", file_url)
        return file_url
    except Exception as e:
        logging.error("Error uploading file to S3: %s", e)
        raise
