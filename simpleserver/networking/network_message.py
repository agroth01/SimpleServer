MESSAGE_PREFIX = "$"
HEADER_SEPARATOR = "|"
BODY_SEPARATOR = "%"

class NetworkMessage:
    def __init__(self):
        self.headers = []
        self.body = ""

    def add_header(self, header_name, value=None):
        """
        Adds a header to the message.
        """
        self.headers.append(Header(header_name, value))

    def has_header(self, header_name):
        """
        Checks if the message has a header with the given name.
        """
        for header in self.headers:
            if header.name == header_name:
                return True
        return False

    def get_header(self, header_name):
        """
        Gets the header with the given name.
        """
        for header in self.headers:
            if header.name == header_name:
                return header
        return None

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
            serialized += str(header) + HEADER_SEPARATOR
        serialized += BODY_SEPARATOR + self.body
        return serialized

    def __deserialize(self, serialized):
        """
        Deserializes the headers and body from a string.
        """
        # remove prefix
        serialized = serialized[1:]

        # split into headers and body
        split = serialized.split(BODY_SEPARATOR)
        headers = split[0]
        body = split[1]

        # add headers
        for header in headers.split(HEADER_SEPARATOR):
            if header == "":
                continue
            split = header.split(":")
            self.add_header(Header(split[0], split[1]))

        # set body
        self.set_body(body)

class Header:
    """
    Represents a header in a network message.
    """
    def __init__(self, name, value=""):
        self.name = name
        self.value = value

    def __str__(self):
        return self.name + ":" + self.value