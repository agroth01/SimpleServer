# SimpleServer
A simple socket server client library for python. This library is meant to abstract the creation of a server-client system on a very
high level. This was originally created for my python voice chat project, but after finding myself starting a new project with the same
needs, I asbtracted it into it's own module for ease of use in the future.

# Overview
### Server
```python
from simpleserver import SimpleServer
from simpleserver.networking import NetworkMessage

def on_message(client, message):

    if message.has_header("handshake"):
        # create a response to hands
        response = NetworkMessage()
        response.add_header("handshake", value="example")
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
By design, the client implementation is a lot more open, to facilitate integration into any application with less restrictions.
```python
from simpleserver import SimpleClient
from simpleserver.networking import NetworkMessage

# Create a new client instance.
client = SimpleClient()

# attempt to connect to a server.
success, message = client.connect("localhost", 8080)

if success:
    # If the connection was successful, we can send a message to the server.
    message = NetworkMessage()
    message.add_header("handshake")
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

### NetworkMessage
To allow for more flexible and easy communication between the server and client, the class NetworkMessage is used instead of sending raw data yourself. An instance of NetworkMessage consists of headers and a body

Since not all messages are meant to be handled the same way, headers are a great way to categorize messages and describe their properties. A NetworkMessage does not need a header. Headers do not need a value either, but all headers require a name.
```python
# a network message can contain multiple headers if needed.
message = NetworkMessage()
message.add_header("no_value_header")
message.add_header("value_header" value="this is a value")

# headers can also be looked up and retrieved from any networkmessage
message.has_header("no_value_header") # True

message.get_header("value_header") # Returns Header instance
message.get_header("another_name") # Returns None
```

The body of the header is used to send the actual data of the message. Like the header, this is not required for a NetworkMessage.
```python
message = NetworkMessage()
message.set_body("any string can be in the body. will be converted into bytes when sent")

# the body of a message can be accessed via the body property. if a message has no body, this will be an empty string.
print(message.body)
```
