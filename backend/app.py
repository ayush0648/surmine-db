from flask import Flask
from flask_cors import CORS
from routes.project_files import project_files_bp
from routes.registrar import registrar_bp  # Import the registrar blueprint

app = Flask(__name__)

CORS(app)

@app.route("/")
def serve_index():
    return send_from_directory(app.static_folder, "index.html")

@app.route("/<path:path>")
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

# Register blueprints
app.register_blueprint(project_files_bp, url_prefix="/project-files")
app.register_blueprint(registrar_bp, url_prefix="/registrar")  # Add registrar blueprint

if __name__ == "__main__":
    app.run(debug=True)
