from flask import Blueprint, request, jsonify
from backend.utils.s3_utils import upload_file_to_s3, BUCKET_NAME
import os
from datetime import datetime
import logging
from backend.utils.s3_utils import list_s3_directories


project_files_bp = Blueprint('project_files', __name__)

# Add logging
logging.basicConfig(level=logging.DEBUG)

@project_files_bp.route("/upload-multiple", methods=["POST"])
def upload_multiple_files():
    customer = request.form.get("customer")
    project = request.form.get("project")
    folder = request.form.get("folder")  # Optional: Subfolder name within the project
    files = request.files.getlist("files")  # Handle multiple file uploads

    # Log the incoming data for debugging
    logging.debug("Received customer: %s, project: %s, folder: %s", customer, project, folder)
    logging.debug("Received files: %s", [f.filename for f in files])

    if not customer or not project or not files:
        return jsonify({"error": "Missing required fields"}), 400

    uploaded_files = []
    for file in files:
        original_filename = file.filename
        file_extension = os.path.splitext(original_filename)[1]
        current_time = datetime.now().strftime("%d%m%Y_%H%M%S")
        new_filename = f"{os.path.splitext(original_filename)[0]}_{current_time}{file_extension}"

        # Construct S3 Key
        key = f"customers/{customer}/{project}/{folder}/{new_filename}" if folder else f"customers/{customer}/{project}/{new_filename}"

        # Log file name and key
        logging.debug("Uploading file: %s with key: %s", original_filename, key)

        try:
            s3_url = upload_file_to_s3(file, key)
            uploaded_files.append({"file_name": original_filename, "url": s3_url})
        except Exception as e:
            logging.error("Error uploading file %s: %s", original_filename, e)
            return jsonify({"error": "File upload failed"}), 500

    return jsonify({"uploaded_files": uploaded_files}), 200

@project_files_bp.route("/list-customers", methods=["GET"])
def list_customers():
    try:
        customers = list_s3_directories("customers/")  # Prefix to list customer folders
        return jsonify({"customers": customers}), 200
    except Exception as e:
        print(f"Error listing customers: {str(e)}")  # Log the error for Heroku logs
        return jsonify({"error": "Failed to list customers"}), 500


@project_files_bp.route("/list-projects/<customer>", methods=["GET"])
def list_projects(customer):
    prefix = f"customers/{customer}/"
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Delimiter="/", Prefix=prefix)
        projects = [prefix['Prefix'].split('/')[2] for prefix in response.get('CommonPrefixes', [])]
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@project_files_bp.route("/list-files/<customer>/<project>", methods=["GET"])
def list_files(customer, project):
    prefix = f"customers/{customer}/{project}/"
    try:
        response = s3.list_objects_v2(Bucket=BUCKET_NAME, Prefix=prefix)
        files = [obj['Key'].split('/')[-1] for obj in response.get('Contents', [])]
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": str(e)}), 500