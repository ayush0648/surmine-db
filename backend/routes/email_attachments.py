from flask import Blueprint, request, jsonify

# Create the Blueprint for email attachments
email_attachments_bp = Blueprint('email_attachments', __name__)

@email_attachments_bp.route('/upload', methods=['POST'])
def upload_attachment():
    # Your logic for handling attachment upload
    return jsonify({"message": "Attachment uploaded successfully"})
