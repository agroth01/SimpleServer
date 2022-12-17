import threading
import socket
import time
from src.server.server_logging import Logger, LoggingLevel
from src.server.client_connection import ClientConnection
from src.networking.network_message import NetworkMessage

DEFAULT_TICK_RATE = 120

class SimpleServer:
    def __init__(self, host, port, verbose_logging=False, use_timestamps=True, tick_rate=DEFAULT_TICK_RATE,
                 manual_update=False):
        self.host = host
        self.port = port
        self.manual_update = manual_update

        self.logger = Logger(verbose=verbose_logging, 
                            use_timestamps=use_timestamps)

        self.update_frequency = 1 / tick_rate

        # define callbacks
        self.on_connection = ServerCallback()
        self.on_message = ServerCallback()
        self.on_disconnect = ServerCallback()
        self.on_update = ServerCallback()

        self.clients = []

        self.stop_flag = False

    def start(self):
        """
        Starts the server with a blocking call.
        """
        self.__internal_start()

    def stop(self):
        """
        Flags the server to stop.
        """
        self.stop_flag = True

    def start_async(self):
        """
        Starts the server with a non-blocking call.
        Returns the thread object.
        """
        thread = threading.Thread(target=self.__internal_start)
        thread.start()
        return thread

    def set_tick_rate(self, tick_rate):
        """
        Sets the tick rate of the server.
        """
        self.update_frequency = 1 / tick_rate  

    def update(self):
        """
        Update the logic of the server.
        """
        self.__handle_new_connections()
        self.__update_existing_connections()
        self.on_update.invoke()

    def broadcast(self, message, exclusions=[]):
        """
        Broadcasts a message to all clients.
        """
        for client in self.clients:
            if client not in exclusions:
                client.send(message)

    def get_clients(self):
        """
        Returns a list of all clients.
        """
        return self.clients

    def messsage_clients(self, clients, message):
        """
        Sends a message to a list of clients.
        """
        for client in clients:
            client.send(message)

    def __internal_start(self):
        """
        Internal method to start the server.
        """
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.host, self.port))
        self.socket.listen()
        self.socket.setblocking(False)
        self.logger.log(f"{self.host}:{self.port} is listening...", LoggingLevel.DEBUG)

        # start the main loop as long as server is not set to manual updating mode
        if not self.manual_update:
            self.__internal_loop()

    def __internal_loop(self):
        """
        The main loop of the server. Is responsible for accepting connections and
        handling messages from connected clients.
        """
        while not self.stop_flag:
            start_time = time.time()

            # updates the server. in manual update mode, this method is called externally
            self.update()

            self.__limit_frequency(start_time, time.time())

    def __limit_frequency(self, start_time, end_time):
        """
        Limits the frequency of the loop.
        """
        elapsed_time = end_time - start_time
        if elapsed_time < self.update_frequency:
            time.sleep(self.update_frequency - elapsed_time)

    def __handle_new_connections(self):
        """
        Attempts to accept a new connection.
        """
        try:
            connection, address = self.socket.accept()
            client = ClientConnection(connection, address)
            self.clients.append(client)
            self.on_connection.invoke(client)
            self.logger.log(f"New connection from {address}", LoggingLevel.DEBUG)

        except socket.error:
            pass

    def __update_existing_connections(self):
        """
        Updates all existing connections.
        """
        for client in self.clients:
            success, message = client.read()
            if success:
                # we need to test if the message is empty.
                # if it is, we don't want to invoke the callback.
                if message != "":
                    # convert message into network message
                    message = NetworkMessage.decode(message)
                    self.on_message.invoke(client, message)
                    self.logger.log(f"Message from {client.address}: {message.body}", LoggingLevel.DEBUG)
            else:
                self.clients.remove(client)
                self.on_disconnect.invoke(client)
                self.logger.log(f"Client {client.address} disconnected", LoggingLevel.DEBUG)

class ServerCallback:
    def __init__(self):
        self.listeners = []

    def add_listener(self, listener):
        """
        Adds a listener to the list of listeners.
        """
        self.listeners.append(listener)

    def invoke(self, *args, **kwargs):
        """
        Invokes all listeners with the given arguments.
        """
        for listener in self.listeners:
            listener(*args, **kwargs)

    def remove_listener(self, listener):
        """
        Removes a listener from the list of listeners.
        """
        self.listeners.remove(listener)