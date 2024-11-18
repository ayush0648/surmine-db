from flask import Flask
from flask_cors import CORS
from project_files.routes import project_files_bp
from email_data.routes import email_data_bp

app = Flask(__name__)
CORS(app)  # Enable Cross-Origin Resource Sharing

# Register Blueprints
app.register_blueprint(project_files_bp, url_prefix='/project_files')
app.register_blueprint(email_data_bp, url_prefix='/email_data')

@app.route('/')
def index():
    return {"message": "Welcome to the Backend API"}

if __name__ == '__main__':
    app.run(debug=True)
