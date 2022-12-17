import socket
from src.networking.network_message import NetworkMessage

class SimpleClient:
    """
    Simple client class for connection to the simpleserver.
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setblocking(False)

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
            # if we are sending a network message, use the encode method
            if type(message) == NetworkMessage:
                self.socket.send(message.encode())

            # if sending regular data, use standard encoding
            else:
                self.socket.send(message.encode("utf-8"))
            return (True, "Message sent")
        except Exception as e:
            return (False, str(e))

    def read(self):
        """
        Attempts to read a message from the server.
        """
        try:
            data = self.socket.recv(1024)
            if not data:
                return None
            # convert message into network message
            data = NetworkMessage.decode(data)
            return data
        except Exception as e:
            return None