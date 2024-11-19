from flask import Blueprint, jsonify
from .zoho_utils import fetch_and_process_emails

# Define the blueprint for email data routes
email_data_bp = Blueprint('email_data', __name__)

@email_data_bp.route('/fetch', methods=['POST'])
def fetch_emails():
    """
    Fetch emails from Zoho's POP3 server, process attachments,
    upload them to S3, and delete processed emails from the server.
    """
    try:
        # Call the fetch_and_process_emails function
        response = fetch_and_process_emails()
        return jsonify(response)
    except Exception as e:
        # Handle errors and return an appropriate response
        return jsonify({"error": str(e)}), 500
