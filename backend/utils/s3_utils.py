import boto3
import os
import logging
from botocore.exceptions import ClientError

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Log environment variables to ensure they're set
logging.debug("AWS_ACCESS_KEY_ID: %s", os.getenv("AWS_ACCESS_KEY_ID"))
logging.debug("AWS_SECRET_ACCESS_KEY: %s", os.getenv("AWS_SECRET_ACCESS_KEY"))
logging.debug("AWS_REGION: %s", os.getenv("AWS_REGION"))
logging.debug("S3_BUCKET_NAME: %s", os.getenv("S3_BUCKET_NAME"))

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
    endpoint_url='https://s3.ap-south-1.amazonaws.com'
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def upload_file_to_s3(file_obj, key):
    try:
        logging.debug("Uploading file to S3 with key: %s", key)
        s3.upload_fileobj(file_obj, BUCKET_NAME, key)
        file_url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
        logging.debug("File uploaded successfully: %s", file_url)
        return file_url
    except ClientError as e:
        # Capture AWS-specific error codes
        error_code = e.response['Error']['Code']
        error_message = e.response['Error']['Message']
        logging.error("AWS error occurred: %s - %s", error_code, error_message)
        raise
    except Exception as e:
        # Catch other exceptions
        logging.error("An unexpected error occurred: %s", e)
        raise
