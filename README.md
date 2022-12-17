# SimpleServer
A simple socket server client library for python. This library is meant to abstract the creation of a server-client system on a very
high level. This was originally created for my python voice chat project, but after finding myself starting a new project with the same
needs, I asbtracted it into it's own module for ease of use in the future.

# Basic example
### Server
```python
from simpleserver import SimpleServer
from simpleserver.networking import NetworkMessage, Header

def on_message(client, message):
    # all messages are instances of NetworkMessage. This class has
    # a body and multiple headers. The body is a string, the headers
    # are instances of Header. The header class has a name and a value.
    if message.has_header("handshake"):
        # here we see that the client sent a message with a header
        # named "handshake". We will send a message back to the client
        # with a header named "handshake" and a value of "example".
        response = NetworkMessage()

        # headers need a name. value is optional.
        response.add_header(Header("handshake", value="example"))
        response.set_body("Hello from the server!")

        # send the message back to the client. seralization and encoding
        # is handled automatically. messages can also be raw bytes, it does
        # not have to be a NetWorkMessage instance. However, the client will
        # automatically decode the message as a NetworkMessage instance with
        # no header.
        client.send(response)

    print(f"Message received from {client.address}: {message.body}")

    
# Create a new server instance.
server = SimpleServer("localhost", 8080, tick_rate=120)

# The server works on callbacks. You will need to register a callback
# to desired events. The following callback will be called when a client
# sends a message to the server.
server.on_message.add_listener(on_message)

# start the server instance. This will block the current thread
# for a non blocking version, use start_async() instead.
server.start()
```

### Client
```python
from simpleserver import SimpleClient
from simpleserver.networking import NetworkMessage, Header

# Create a new client instance.
client = SimpleClient()

# Connect to a server. This returns a touple of (success, message)
# that can be used to determine if the connection was successful.
success, message = client.connect("localhost", 8080)

if success:
    # If the connection was successful, send a handshake message.
    message = NetworkMessage()
    message.add_header(Header("handshake"))
    message.set_body("Hello server!")

    # send the message to the server. Just like the server, you can also
    # send raw bytes instead of a NetworkMessage instance.
    client.send(message)

    # start a loop to receive messages from the server.
    while True:
        # here we attempt to read a message from the server. If there is
        # no message, the read() method will return None.
        message = client.read()
        if message:
            if message.has_header("handshake"):
                print("Server handshake received")

else:
    # If the connection was unsuccessful, print the error message.
    print(f"Connection failed: {message}")
```
