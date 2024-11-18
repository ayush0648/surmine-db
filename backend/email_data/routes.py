from flask import Blueprint, request, jsonify
from .zoho_utils import fetch_zoho_emails, download_attachments
from .s3_utils import upload_file_to_s3

email_data_bp = Blueprint('email_data', __name__)

@email_data_bp.route('/fetch', methods=['POST'])
def fetch_emails():
    emails = fetch_zoho_emails()
    email_metadata = []

    for email in emails:
        attachments = download_attachments(email['id'])
        for attachment in attachments:
            file_path = f"emails/{email['id']}/{attachment['file_name']}"
            s3_url = upload_file_to_s3(attachment['file_content'], file_path)
            email_metadata.append({
                "email_id": email['id'],
                "subject": email['subject'],
                "attachment_url": s3_url
            })

    return jsonify({"message": "Emails processed successfully", "email_metadata": email_metadata})