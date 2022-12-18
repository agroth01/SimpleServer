from simpleserver.networking.network_message import NetworkMessage

class ClientConnection:
    """
    Representation of a socket connection to a client.
    """
    def __init__(self, socket, address):
        self.socket = socket
        self.address = address

    def read(self):
        """
        Attempts to read a message from the client.
        Will return a tuple with format (success, message).
        If success if false, it means socket is closed.
        """
        try:
            data = self.socket.recv(1024)
            if not data:
                return (False, "Socket closed")
            return (True, data)
        except Exception as e:
            if e.errno == 10035:
                return (True, "")
            return (False, str(e))

    def send(self, message):
        """
        Attempts to send a message to the client.
        Will return a tuple with format (success, message).
        If success if false, it means socket is closed.
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


    def __str__(self) -> str:
        """
        String representation of the client connection.
        Returns the address of the client.
        """
        return str(self.address)