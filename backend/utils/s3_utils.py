import boto3
import os

s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

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
