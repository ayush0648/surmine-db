from flask import Blueprint, request, jsonify
from utils.s3_utils import upload_file_to_s3
from utils.excel_utils import get_serial_number_and_update, fetch_records

registrar_bp = Blueprint("registrar", __name__)

# Paths to Excel files
INCOMING_SHEET_PATH = "path_to_excel/incoming_registrar.xlsx"
DISPATCH_SHEET_PATH = "path_to_excel/dispatch_registrar.xlsx"

@registrar_bp.route("/upload", methods=["POST"])
def upload_file():
    record_type = request.form.get("record_type")  # "incoming" or "dispatch"
    details = request.form.to_dict(flat=True)
    file = request.files.get("file")

    if not record_type or not file:
        return jsonify({"error": "Missing required fields"}), 400

    # Determine the correct Excel file
    sheet_path = INCOMING_SHEET_PATH if record_type == "incoming" else DISPATCH_SHEET_PATH

    # Generate serial number and update Excel sheet
    serial_number = get_serial_number_and_update(sheet_path, details)

    # Upload file to S3 under the serial number folder
    key = f"{record_type}/{serial_number}/{file.filename}"
    s3_url = upload_file_to_s3(file, key)

    return jsonify({"message": "File uploaded successfully", "serial_number": serial_number, "url": s3_url})

@registrar_bp.route("/records", methods=["GET"])
def get_records():
    record_type = request.args.get("record_type")  # "incoming" or "dispatch"

    if not record_type:
        return jsonify({"error": "Missing required parameters"}), 400

    # Determine the correct Excel file
    sheet_path = INCOMING_SHEET_PATH if record_type == "incoming" else DISPATCH_SHEET_PATH

    # Fetch records from the sheet
    records = fetch_records(sheet_path)
    return jsonify(records)
