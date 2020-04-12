from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EmailSender:
    def __init__(self, sender_address, password, receiver_address):
        self._sender_address = sender_address
        self._receiver_address = receiver_address
        self._password = password

    def send_email(self, subject, text):
        email = self._generate_email(subject, text)

    def _generate_email(self, email_subject, email_text):
        email_message = MIMEMultipart("multipart")
        email_message["From"] = self._sender_address
        email_message["To"] = self._receiver_address
        email_message["Subject"] = email_subject

        msg_body = MIMEText(email_text)
        email_message.attach(msg_body)

        return email_message


if __name__ == '__main__':
    sender = EmailSender("Sender_test@address", "test_password", "Test@address")
