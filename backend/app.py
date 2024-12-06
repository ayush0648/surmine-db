from flask import Flask
from routes.project_files import project_files_bp
from routes.registrar import registrar_bp  # Import the registrar blueprint

app = Flask(__name__)

# Register blueprints
app.register_blueprint(project_files_bp, url_prefix="/project-files")
app.register_blueprint(registrar_bp, url_prefix="/registrar")  # Add registrar blueprint

if __name__ == "__main__":
    app.run(debug=True)
