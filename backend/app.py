from flask import Flask
from flask_cors import CORS
from backend.routes.project_files import project_files_bp
from flask import send_from_directory
import os

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

if __name__ == "__main__":
    app.run(debug=True)
