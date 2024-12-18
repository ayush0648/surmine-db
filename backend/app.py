from flask import Flask
from flask_cors import CORS
from backend.routes.project_files import project_files_bp
from flask import send_from_directory
import os

app = Flask(__name__, static_folder='static')

CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory(os.path.join(app.root_path, 'frontend'), "index.html")

# Serve static files (JavaScript and CSS) from the frontend folder
@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(os.path.join(app.root_path, 'frontend'), path)

# Register blueprints
app.register_blueprint(project_files_bp, url_prefix="/project-files")

if __name__ == "__main__":
    app.run(debug=True)
