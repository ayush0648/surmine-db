from flask import Blueprint, jsonify, request
from backend.utils.s3_utils import list_s3_directories, list_s3_files, upload_file_to_s3

project_files_bp = Blueprint("project_files", __name__)

# List customers
@project_files_bp.route("/list-customers", methods=["GET"])
def list_customers():
    try:
        customers = list_s3_directories("customers/")
        return jsonify({"customers": customers})
    except Exception as e:
        return jsonify({"error": f"Error listing customers: {str(e)}"}), 500

# List projects for a specific customer
@project_files_bp.route("/list-projects/<string:customer>", methods=["GET"])
def list_projects(customer):
    try:
        projects = list_s3_directories(f"customers/{customer}/")
        return jsonify({"projects": projects})
    except Exception as e:
        return jsonify({"error": f"Error listing projects for {customer}: {str(e)}"}), 500

# List files for a specific project
@project_files_bp.route("/list-files/<string:customer>/<string:project>", methods=["GET"])
def list_files(customer, project):
    try:
        files = list_s3_files(f"customers/{customer}/{project}/")
        return jsonify({"files": files})
    except Exception as e:
        return jsonify({"error": f"Error listing files for {project}: {str(e)}"}), 500

# Upload multiple files
@project_files_bp.route("/upload-multiple", methods=["POST"])
def upload_multiple_files():
    customer = request.form.get("customer")
    project = request.form.get("project")
    folder = request.form.get("folder")  # Optional: Subfolder within the project
    files = request.files.getlist("files")  # Handle multiple file uploads

    if not customer or not project or not files:
        return jsonify({"error": "Missing required fields"}), 400

    uploaded_files = []
    for file in files:
        try:
            # Generate S3 key
            key = f"customers/{customer}/{project}/"
            if folder:
                key += f"{folder}/"
            key += file.filename

            # Upload file
            s3_url = upload_file_to_s3(file, key)
            uploaded_files.append({"file_name": file.filename, "url": s3_url})
        except Exception as e:
            return jsonify({"error": f"Failed to upload file: {file.filename}. Error: {str(e)}"}), 500

    return jsonify({"message": "Files uploaded successfully", "files": uploaded_files})
