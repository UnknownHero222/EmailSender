from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib


class EmailSender:
    def __init__(self, sender_address, password, receiver_address):
        self._sender_address = sender_address
        self._receiver_address = receiver_address
        self._password = password

        # TODO the moment with the server needs to be thought over more carefully
        self._smtp_server = 'smtp.gmail.com'

    def send_email(self, subject, text):
        email = self._generate_email(subject, text)

        try:
            server = smtplib.SMTP_SSL(self._smtp_server, 465)
            server.ehlo()
            server.login(self._sender_address, self._password)

            server.sendmail(self._sender_address, self._receiver_address, email.as_string())

            server.close()
        except Exception as err:
            print("Error! Sending the message to an email failed. Error: {}".format(err))

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
