import boto3
import os
from botocore.exceptions import NoCredentialsError, PartialCredentialsError

# Load environment variables for AWS credentials and S3 bucket name
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
S3_REGION = os.getenv("S3_REGION", "us-east-1")  # Default region

# Initialize S3 client
def get_s3_client():
    """
    Returns a boto3 S3 client initialized with credentials.
    """
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name=S3_REGION,
    )

def upload_file_to_s3(file_content, file_path):
    """
    Uploads a file to an S3 bucket and returns its public URL.

    :param file_content: The binary content of the file to be uploaded.
    :param file_path: The path where the file will be stored in the S3 bucket.
    :return: The public URL of the uploaded file.
    """
    s3_client = get_s3_client()

    try:
        # Upload the file to the specified path in the bucket
        s3_client.put_object(
            Bucket=S3_BUCKET_NAME,
            Key=file_path,
            Body=file_content,
            ACL="public-read"  # Make the file publicly accessible
        )

        # Construct the public URL for the uploaded file
        s3_url = f"https://{S3_BUCKET_NAME}.s3.{S3_REGION}.amazonaws.com/{file_path}"
        return s3_url

    except NoCredentialsError:
        raise Exception("AWS credentials not found. Check your environment variables.")
    except PartialCredentialsError:
        raise Exception("Incomplete AWS credentials. Ensure both access key and secret key are set.")
    except Exception as e:
        raise Exception(f"Failed to upload file to S3: {str(e)}")
