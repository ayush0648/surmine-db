from flask import Blueprint, request, jsonify
from .s3_utils import upload_file_to_s3
from .dynamodb_utils import save_metadata, fetch_hierarchy

project_files_bp = Blueprint('project_files', __name__)

@project_files_bp.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    customer = request.form['customer']
    project = request.form['project']

    file_path = f"{customer}/{project}/{file.filename}"
    s3_url = upload_file_to_s3(file, file_path)

    metadata = {
        "customer": customer,
        "project": project,
        "file_name": file.filename,
        "file_url": s3_url
    }
    save_metadata(metadata)

    return jsonify({"message": "File uploaded successfully", "s3_url": s3_url})

@project_files_bp.route('/hierarchy', methods=['GET'])
def get_hierarchy():
    data = fetch_hierarchy()
    return jsonify(data)
