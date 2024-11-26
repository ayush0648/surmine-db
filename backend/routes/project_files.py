from flask import Blueprint, request, jsonify
from utils.s3_utils import upload_file_to_s3
import os
from datetime import datetime

project_files_bp = Blueprint('project_files', __name__)

@project_files_bp.route("/upload", methods=["POST"])
def upload_project_file():
    customer = request.form.get("customer")
    project = request.form.get("project")
    file = request.files.get("file")

    if not customer or not project or not file:
        return jsonify({"error": "Missing required fields"}), 400

    # Get the original file name
    original_filename = file.filename

    # Extract the file extension (e.g., .pdf, .jpg)
    file_extension = os.path.splitext(original_filename)[1]

    # Generate a new file name with date and time (ddmmyyyy_hhmmss)
    current_time = datetime.now().strftime("%d%m%Y_%H%M%S")
    new_filename = f"{os.path.splitext(original_filename)[0]}_{current_time}{file_extension}"

    # S3 Key
    key = f"customers/{customer}/{project}/{new_filename}"
    s3_url = upload_file_to_s3(file, key)

    return jsonify({"message": "File uploaded successfully", "url": s3_url})
