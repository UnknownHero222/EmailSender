class EmailSender:
    def __init__(self, address, password):
        self._address = address
        self._password = password


if __name__ == '__main__':
    sender = EmailSender("Test@address", "test_password")
