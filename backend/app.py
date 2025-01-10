from flask import Flask, request, abort, jsonify, send_from_directory
from flask_cors import CORS
from backend.routes.project_files import project_files_bp
import os
from dotenv import load_dotenv
from backend.utils.s3_utils import generate_presigned_url
import zipfile
import io
from backend.utils.s3_utils import list_s3_files, download_s3_file  # Add these utilities.

load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'frontend'))

CORS(app)


# Route to serve index.html
@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

# Route to serve static files (JS, CSS, etc.)
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Register blueprints
app.register_blueprint(project_files_bp, url_prefix="/project-files")

@app.route("/project-files/download-file/<customer>/<project>/<path:filename>", methods=["GET"])
def download_file(customer, project, filename):
    """
    Generate a presigned URL for downloading a specific file.
    """
    try:
        s3_key = f"customers/{customer}/{project}/{filename}"  # Construct the S3 key
        presigned_url = generate_presigned_url(s3_key)  # Generate the URL
        return jsonify({"url": presigned_url}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate download URL: {str(e)}"}), 500


@app.route("/project-files/download-folder/<customer>/<project>", methods=["GET"])
def download_folder(customer, project):
    """
    Download all files in a customer/project folder as a .zip.
    """
    try:
        s3_prefix = f"customers/{customer}/{project}/"  # Define the folder path in S3
        files = list_s3_files(s3_prefix)  # List all files in the folder

        # Create an in-memory zip file
        memory_file = io.BytesIO()
        with zipfile.ZipFile(memory_file, 'w') as zf:
            for file in files:
                file_content = download_s3_file(file)  # Download each file's content
                zf.writestr(os.path.basename(file), file_content)  # Add file to the zip

        memory_file.seek(0)  # Reset the file pointer

        # Return the zip file
        return send_file(
            memory_file,
            as_attachment=True,
            download_name=f"{project}.zip",  # Provide a meaningful name
            mimetype="application/zip"
        )
    except Exception as e:
        return jsonify({"error": f"Failed to download folder: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(debug=True)