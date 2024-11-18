import boto3
import os

# Load environment variables
DYNAMODB_TABLE = os.getenv('DYNAMODB_TABLE')
dynamodb = boto3.resource('dynamodb')

def save_metadata(metadata):
    """
    Saves file metadata to DynamoDB.
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        table.put_item(Item=metadata)
    except Exception as e:
        raise Exception(f"Error saving metadata to DynamoDB: {str(e)}")

def fetch_hierarchy():
    """
    Fetches a hierarchical view of files from DynamoDB.
    """
    try:
        table = dynamodb.Table(DYNAMODB_TABLE)
        response = table.scan()
        items = response.get('Items', [])

        hierarchy = {}
        for item in items:
            customer = item['customer']
            project = item['project']
            file_name = item['file_name']
            file_url = item['file_url']

            if customer not in hierarchy:
                hierarchy[customer] = {}
            if project not in hierarchy[customer]:
                hierarchy[customer][project] = []
            hierarchy[customer][project].append({"file_name": file_name, "file_url": file_url})

        return hierarchy
    except Exception as e:
        raise Exception(f"Error fetching hierarchy: {str(e)}")
