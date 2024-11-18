import boto3
import os

# Load environment variables
S3_BUCKET = os.getenv('S3_BUCKET')
S3_REGION = os.getenv('S3_REGION')

s3_client = boto3.client('s3', region_name=S3_REGION)

def upload_file_to_s3(file, file_path):
    """
    Uploads a file to Amazon S3.
    """
    try:
        s3_client.upload_fileobj(
            file,
            S3_BUCKET,
            file_path,
            ExtraArgs={"ACL": "public-read"}
        )
        s3_url = f"https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com/{file_path}"
        return s3_url
    except Exception as e:
        raise Exception(f"Error uploading file to S3: {str(e)}")
