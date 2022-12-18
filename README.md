# SimpleServer
A simple socket server client library for python. This library is meant to abstract the creation of a server-client system on a very
high level. This was originally created for my python voice chat project, but after finding myself starting a new project with the same
needs, I asbtracted it into it's own module for ease of use in the future.
# Overview

### Server
By design, creating and starting a server should be very simple.
```python
# most basic implementation.
server = Server("localhost", 1234)
server.start()

# optional parameters if needed
server = Server("localhost",
                1234,
                verbose_logging=True, # Will print debug messages. By default it will only display errors and warnings.
                tick_rate = 60,       # Number of desired ticks per second. Defaults to 120.
                manual_update=False)  # When enabled, start will not start server loop. This will then have do be done manually via calling server.update()
                
# This is a blocking call to start the server loop.                
server.start()

# This is a non blocking call to start server loop. Will run server loop on separate thread.
server.start_async()
```

The server is built to have callbacks for events happening. You will have to manually add listeners to these events before starting your server.
```python
def connection_fn(client):
    print(f"Client connected: {client.address}")

def message_fn(client, message):
    print(f"Message received from {client.address}: {message.body}")

def disconnect_fn(client):
    print(f"Client disconnected: {client.address}")
    
def update_fn():
    pass
    
# on_connection event will be called when a new client connects to the server.
server.on_connection.add_listener(connection_fn)   

# on_message event will be called when a client sends a message to the server.
# the message received will be a NetworkMessage object.
server.on_message.add_listener(message_fn)
 
# on_disconnect event will be called when a client loses connection to the server.
server.on_disconnect.add_listener(disconnect_fn)

# on_update is called each time the server goes through an update cycle. this is useful if you want to perform some operation each cycle.
server.on_update.add_listener(update_fn)
```

Sending message to clients can be done in multiple ways.
```python
# sending a message directly to a ConnectionClient instance
client.send(message)

# sending a message to select clients.
# list of all clients can be retrieved via server.get_clients() if needed.
targets = [client1, client2, client5]
server.message_clients(targets, message)

# broadcasting a message to all clients. optional list of excluded clients can be passed.
server.broadcast(message)
server.broadcast(message, exclusions=[client4])
```

### Client
In order to not restrict developers in how they implement their client, the SimpleClient class is more open to how it is used.
```python
# create the instance of the client. this does not connect to anything, as you might want to connect later.
client = SimpleClient()

# attempt to connect to a server by ip and port. this method will return a bool indicating if the connection
# was succesfull or not, as well as a message for handling cases where connection could not be established.
success, message = client.connect("localhost", 1234)
```

Besides connecting to a server, the client only exposes two high level methods for sending and receiving data from the server. How and when you chose to call these are up to the specific needs of the application.
```python
# this will send a NetworkMessage to the server. it should be noted that you can also send raw bytes directly, but the server will decode
# the bytes into a headerless NetworkMessage upon reception.
client.send(message)

# calling read() will attempt to receive any data from the server. this will either return
# a NetworkMessage instance or None. You will have to check for this.
data = client.read()
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

# Example
### Server
```python
from simpleserver import SimpleServer
from simpleserver.networking import NetworkMessage

def on_message(client, message):
    if message.has_header("handshake"):
        # create a response to handshake
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

# start the server instance.
server.start()
```

### Client
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
