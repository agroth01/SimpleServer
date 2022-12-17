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

    if message.has_header("handshake"):
        # create a response to hands
        response = NetworkMessage()
        response.add_header(Header("handshake", value="example"))
        response.set_body("Hello from the server!")

        # send the response to the same client that sent the message.
        client.send(response)

    print(f"Message received from {client.address}: {message.body}")

# Create a new server instance.
server = SimpleServer("localhost", 8080, tick_rate=120)

# add a callback to the on_message event.
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

# attempt to connect to a server.
success, message = client.connect("localhost", 8080)

if success:
    # If the connection was successful, we can send a message to the server.
    message = NetworkMessage()
    message.add_header(Header("handshake"))
    message.set_body("Hello server!")

    # send the message.
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
    print(f"Connection failed: {message}")
```
