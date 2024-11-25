from flask import Blueprint, request, jsonify
from utils.s3_utils import upload_file_to_s3
from utils.dynamodb_utils import save_project_file_metadata

project_files_bp = Blueprint('project_files', __name__)

@project_files_bp.route("/upload", methods=["POST"])
def upload_project_file():
    customer = request.form.get("customer")
    project = request.form.get("project")
    file = request.files.get("file")

    if not customer or not project or not file:
        return jsonify({"error": "Missing required fields"}), 400

    # S3 Key
    key = f"customers/{customer}/{project}/{file.filename}"
    s3_url = upload_file_to_s3(file, key)

    # Save metadata to DynamoDB
    metadata = {
        "CustomerID": customer,
        "ProjectID": project,
        "FilePath": key
    }
    save_project_file_metadata(metadata)

    return jsonify({"message": "File uploaded successfully", "url": s3_url})
