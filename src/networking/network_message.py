MESSAGE_PREFIX = "$"
HEADER_SEPARATOR = "|"
BODY_SEPARATOR = "%"

class NetworkMessage:
    def __init__(self):
        self.headers = []
        self.body = ""

    def add_header(self, header):
        """
        Adds a header to the message.
        """
        self.headers.append(header)

    def set_body(self, body):
        """
        Sets the body of the message.
        """
        self.body = body

    def encode(self):
        """
        Encodes the message into bytes meant to be sent over the network.
        """
        return self.__serialize().encode("utf-8")

    @staticmethod
    def decode(data):
        """
        Decodes the message from bytes received over the network.
        """
        message = NetworkMessage()
        message.__deserialize(data.decode("utf-8"))
        return message

    def __serialize(self):
        """
        Serializes the headers and body into a string.
        """
        serialized = MESSAGE_PREFIX
        for header in self.headers:
            serialized += header + HEADER_SEPARATOR
        serialized += BODY_SEPARATOR + self.body + BODY_SEPARATOR
        return serialized

    def __deserialize(self, serialized):
        """
        Deserializes the headers and body from a string.
        """
        serialized = serialized.replace(MESSAGE_PREFIX, "")
        serialized = serialized.replace(BODY_SEPARATOR, "")
        parts = serialized.split(HEADER_SEPARATOR)
        self.headers = parts[:-1]
        self.body = parts[-1]