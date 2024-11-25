import boto3
import os

dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION"),
)

TABLE_NAME = os.getenv("DYNAMODB_TABLE_NAME")

def save_project_file_metadata(metadata):
    table = dynamodb.Table(TABLE_NAME)
    table.put_item(Item=metadata)
