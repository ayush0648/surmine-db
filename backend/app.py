from flask import Flask, request, abort, jsonify, send_from_directory
from flask_cors import CORS
from backend.routes.project_files import project_files_bp
from geopy.distance import geodesic
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=os.path.join(os.getcwd(), 'frontend'))

CORS(app)

# Office location and geofencing configuration
OFFICE_COORDINATES = (28.4577008, 77.0513981)  # Latitude and Longitude of your office
RADIUS_KM = 0.5  # Radius in kilometers


@app.route("/check-location", methods=["POST"])
def check_location():
    """
    Validate user location received from the frontend.
    """
    data = request.get_json()
    user_coordinates = (data.get("latitude"), data.get("longitude"))

    if not all(user_coordinates):
        abort(400, "Invalid location data received.")

    # Calculate distance
    distance = geodesic(OFFICE_COORDINATES, user_coordinates).km
    print(f"Distance from office: {distance} km")

    if distance > RADIUS_KM:
        abort(403, "Access forbidden: You are outside the allowed area.")

    return jsonify({"message": "Access granted."}), 200

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

# Error handler for forbidden access
@app.errorhandler(403)
def forbidden(e):
    return jsonify({"error": "Access forbidden: Your location is not allowed."}), 403

if __name__ == "__main__":
    app.run(debug=True)
