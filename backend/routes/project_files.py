from flask import Blueprint, request, jsonify
from utils.s3_utils import upload_file_to_s3
import os
from datetime import datetime

project_files_bp = Blueprint('project_files', __name__)

@project_files_bp.route("/upload-multiple", methods=["POST"])
def upload_multiple_files():
    customer = request.form.get("customer")
    project = request.form.get("project")
    folder = request.form.get("folder")  # Optional: Subfolder name within the project
    files = request.files.getlist("files")  # Handle multiple file uploads

    if not customer or not project or not files:
        return jsonify({"error": "Missing required fields"}), 400

    uploaded_files = []
    for file in files:
        # Get original file name and extension
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]

        # Generate a unique file name with timestamp
        current_time = datetime.now().strftime("%d%m%Y_%H%M%S")
        new_filename = f"{os.path.splitext(original_filename)[0]}_{current_time}{file_extension}"

        # Construct S3 Key: customers/<customer>/<project>/<folder>/<filename>
        key = f"customers/{customer}/{project}/{folder}/{new_filename}" if folder else f"customers/{customer}/{project}/{new_filename}"

        # Upload file to S3
        s3_url = upload_file_to_s3(file, key)
        uploaded_files.append({"file_name": original_filename, "url": s3_url})

    return jsonify({"message": "Files uploaded successfully", "files": uploaded_files})
