from flask import Flask
from routes.project_files import project_files_bp

app = Flask(__name__)

# Register blueprints
app.register_blueprint(project_files_bp, url_prefix="/project-files")

if __name__ == "__main__":
    app.run(debug=True)

