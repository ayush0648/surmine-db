import poplib
import email
from email.parser import BytesParser
import os
from .s3_utils import upload_file_to_s3

# Load environment variables
ZOHO_POP3_SERVER = "pop.zoho.com"
ZOHO_EMAIL = os.getenv('ZOHO_EMAIL')
ZOHO_PASSWORD = os.getenv('ZOHO_PASSWORD')


def fetch_and_process_emails():
    """
    Connects to Zoho's POP3 server, fetches emails, saves attachments to S3,
    and deletes emails from the server.
    """
    try:
        # Connect to Zoho POP3 server
        mail_server = poplib.POP3_SSL(ZOHO_POP3_SERVER)
        mail_server.user(ZOHO_EMAIL)
        mail_server.pass_(ZOHO_PASSWORD)

        # Fetch the list of emails
        email_list = mail_server.list()[1]

        processed_emails = []
        for email_info in email_list:
            email_id, _ = email_info.decode().split()
            raw_email = b"\n".join(mail_server.retr(int(email_id))[1])

            # Parse the email
            message = BytesParser().parsebytes(raw_email)

            # Process attachments
            for part in message.walk():
                if part.get_content_disposition() == 'attachment':
                    file_name = part.get_filename()
                    file_content = part.get_payload(decode=True)

                    # Upload attachment to S3
                    s3_path = f"emails/{message['Message-ID']}/{file_name}"
                    s3_url = upload_file_to_s3(file_content, s3_path)

                    processed_emails.append({
                        "email_subject": message['Subject'],
                        "attachment_url": s3_url
                    })

            # Delete email from Zoho server after processing
            mail_server.dele(int(email_id))

        # Close the connection
        mail_server.quit()

        return {"message": "Emails processed and deleted successfully", "data": processed_emails}

    except Exception as e:
        raise Exception(f"Error fetching and processing emails: {str(e)}")
