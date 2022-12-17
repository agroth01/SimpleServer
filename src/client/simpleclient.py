import socket

class SimpleClient:
    """
    Simple client class for connection to the simpleserver.
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self, host, port):
        """
        Attempts to connect to the server.
        Will return a tuple with format (success, message)
        """
        try:
            self.socket.connect((host, port))
            return (True, "Connection successful")
        except Exception as e:
            return (False, str(e))

    def send(self, message):
        """
        Attempts to send a message to the server.
        Will return a tuple with format (success, message)
        """
        try:
            self.socket.send(message.encode("utf-8"))
            return (True, "Message sent")
        except Exception as e:
            return (False, str(e))