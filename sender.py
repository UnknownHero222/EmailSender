import sys
import smtplib
import argparse
import os
import tempfile
import shutil
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.application import MIMEApplication


class EmailSender:
    def __init__(self, sender_address, password, receiver_address, smtp_server):
        self._sender_address = sender_address
        self._receiver_address = receiver_address
        self._password = password
        self._smtp_server = smtp_server

    def send_email(self, email_data):
        email = self._generate_email(email_data)

        try:
            server = smtplib.SMTP_SSL(self._smtp_server, 465)
            server.ehlo()
            server.login(self._sender_address, self._password)

            server.sendmail(self._sender_address, self._receiver_address, email.as_string())

            server.close()
        except Exception as err:
            print("Error! Sending the message to an email failed. Error: {}".format(err))

    def _generate_email(self, email_data):
        email_message = MIMEMultipart("multipart")
        email_message["From"] = self._sender_address
        email_message["To"] = self._receiver_address
        email_message["Subject"] = email_data["subject"]

        msg_body = MIMEText(email_data["text"])
        email_message.attach(msg_body)

        for attached_image in email["images"]:
            with open(attached_image, "rb") as file:
                image = MIMEImage(file.read(), name="image{}.jpg".format(image["images"].index(attached_image)))
                email_message.attach(image)

            shutil.rmtree(os.path.dirname(attached_image))

        for attachment in email["attachments"]:
            with open(attachment, "rb") as file:
                curr_attachment = MIMEApplication(file.read())
                curr_attachment.add_header('Content-Disposition', 'attachment', filename=os.path.basename(doc))
                email_message.attach(curr_attachment)

            shutil.rmtree(os.path.dirname(attachment))

        return email_message


def get_parser():
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument("-s", "--sender", help="e-mail address of the sender")
    args_parser.add_argument("-p", "--password", help="password for the sender's email account")
    args_parser.add_argument("-r", "--receiver", help="e-mail address of the recipient")
    args_parser.add_argument("--smtp", help="address of the SMTP server")

    return args_parser


if __name__ == '__main__':
    parser = get_parser()
    namespace = parser.parse_args(sys.argv[1:])

    sender = EmailSender(namespace.sender, namespace.password, namespace.receiver, namespace.smtp)
    email = {"subject": "Simple e-mail", "text": "Simple text in e-mail body", "images": [], "attachments": []}
    sender.send_email(email)
