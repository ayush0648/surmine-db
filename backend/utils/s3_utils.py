import boto3
import os
from botocore.exceptions import ClientError


s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def generate_presigned_url(s3_key):
    s3_client = boto3.client('s3')
    bucket_name = "your-bucket-name"
    try:
        return s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket_name, 'Key': s3_key},
            ExpiresIn=3600  # URL expiration time in seconds
        )
    except ClientError as e:
        print(f"Error generating presigned URL: {e}")
        return None

# List directories (folders) in S3
def list_s3_directories(prefix):
    result = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix, Delimiter="/")
    return [
        folder.get("Prefix").split("/")[-2]
        for folder in result.get("CommonPrefixes", [])
    ]

# List files in an S3 directory
def list_s3_files(prefix):
    result = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
    return [
        obj["Key"].split("/")[-1]
        for obj in result.get("Contents", [])
        if not obj["Key"].endswith("/")
    ]

# Upload a file to S3
def upload_file_to_s3(file_obj, key):
    s3.upload_fileobj(file_obj, BUCKET_NAME, key)
    return f"https://{BUCKET_NAME}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"

def download_s3_file(s3_key):
    s3_client = boto3.client('s3')
    bucket_name = "your-bucket-name"
    try:
        response = s3_client.get_object(Bucket=bucket_name, Key=s3_key)
        return response['Body'].read()
    except ClientError as e:
        print(f"Error downloading S3 file: {e}")
        return None