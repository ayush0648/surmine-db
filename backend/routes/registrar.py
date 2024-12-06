from flask import Blueprint, request, jsonify
from utils.s3_utils import upload_file_to_s3
from utils.excel_utils import get_serial_number_and_update

registrar_bp = Blueprint("registrar", __name__)

EXCEL_PATH = "path_to_excel/Despatch Registrar.xlsx"  # Update with actual path

@registrar_bp.route("/upload", methods=["POST"])
def upload_file_with_serial_number():
    record_type = request.form.get("record_type")  # Either "dispatch" or "incoming"
    details = request.form.to_dict(flat=True)  # Extract all form details
    file = request.files.get("file")

    if not record_type or not file:
        return jsonify({"error": "Missing required fields"}), 400

    # Get serial number and update Excel sheet
    serial_number = get_serial_number_and_update(EXCEL_PATH, record_type, details)

    # Upload file to S3 under the serial number folder
    key = f"{record_type}/{serial_number}/{file.filename}"
    s3_url = upload_file_to_s3(file, key)

    return jsonify({"message": "File uploaded successfully", "serial_number": serial_number, "url": s3_url})

@registrar_bp.route("/records", methods=["GET"])
def fetch_records():
    record_type = request.args.get("record_type")  # "dispatch" or "incoming"

    wb = openpyxl.load_workbook(EXCEL_PATH)
    sheet = wb.active

    # Extract all records for the given type
    records = []
    for row in sheet.iter_rows(values_only=True):
        if row[0].startswith(record_type.upper()):
            records.append({"serial_number": row[0], "details": row[1:]})

    return jsonify(records)