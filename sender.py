import sys
import smtplib
import argparse
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


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
    email = {"subject": "Simple e-mail", "text": "Simple text in e-mail body"}
    sender.send_email(email)
