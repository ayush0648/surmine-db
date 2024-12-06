import openpyxl

def get_serial_number_and_update(sheet_path, record_type, details):
    """
    Fetch the next serial number from the Excel sheet and update it with details.

    Args:
        sheet_path (str): Path to the Excel sheet.
        record_type (str): Either 'dispatch' or 'incoming'.
        details (dict): Record details to update.

    Returns:
        str: The serial number used.
    """
    wb = openpyxl.load_workbook(sheet_path)
    sheet = wb.active

    # Find the next available row
    next_row = sheet.max_row + 1
    serial_number = f"{record_type.upper()}-{next_row:04d}"  # Example: DISPATCH-0001

    # Write the details to the next row
    sheet.append([serial_number] + [details.get(col, "") for col in details.keys()])

    # Save the updated workbook
    wb.save(sheet_path)

    return serial_number