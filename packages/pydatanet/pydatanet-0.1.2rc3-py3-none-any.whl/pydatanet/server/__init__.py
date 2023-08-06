import enum
import socket
import threading
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOCK_DGRAM, SOL_SOCKET

from pydatanet.server.client import Client
from pydatanet.data import encode, decode

class ServerType(enum.Enum):
    TCP = 0
    UDP = 1

class ServerStatus(enum.Enum):
    NOINIT = 0
    INIT = 1

BUFFER_SIZE = 1048

class Server:
    """
    The base class for creating your own server.
    This client creates a blank server that does nothing, just sits idle. You must call `Server.connect()` in order for the server to switch to
    it's active state. You can check the server's status using `Server.getStatus()`

    :params:
    host: The IP address to bind this server to.
    port: The port to bind this server to.
    serverType: The socket protocol to use, UDP or TCP. (defaults to `ServerType.TCP`)
    maxConn: The maximum amount of clients that can join at a time, in order to prevent DDOS attacks [TCP ONLY!] and prevent crashes, even from legitimate clients. (defaults to 256, you can lower or higher this based on your host specs)

    :return:
    `None`
    """
    def __init__(self, host: str, port: int, serverType = ServerType.TCP, maxConn: int = 256):
        self.host = host
        self.port = port
        self.socket = None
        self.maxConn = maxConn
        self.status = ServerStatus.NOINIT
        self.clients = []
        self.serverType = serverType

        self.dataReceiveListeners = []
        self.onJoinListeners = []

        if serverType == ServerType.TCP:
            self.socket = socket.socket(AF_INET, SOCK_STREAM)
        elif serverType == ServerType.UDP:
            self.socket = socket.socket(AF_INET, SOCK_DGRAM)
        else:
            raise ValueError(f"Invalid server type '{serverType}'")

        self.socket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

    def on_recv(self, sender, data):
        """
        Triggered when someone sends a packet. Do not explicitly trigger as unexpected behaviour may occur.

        :return:
        `None`
        """
        data = decode(data)
        for listenFunc in self.dataReceiveListeners:
            listenFunc(sender, data)

    def getStatus(self):
        """
        Get the current status of the server.

        :return:                            
        `pydatanet.server.status` status
        """
        return self.status

    def getClients(self):
        """
        Return a list of every single client currently connected.

        :return:
        `list` clients
        """
        return self.clients

    def on_recv_bind(self, func):
        """
        Bind a function to when someone sends data.

        :params:
        `function/lambda` func

        :return:
        `None`
        """
        self.dataReceiveListeners.append(func)

    def connect(self, autoPoll: bool = True):
        """
        Bind to that socket and start listening for connections.

        :params:
        `bool` autoPoll: whether the server should go into 'heartbeat' mode in order to process connections, disable if you want to attach `Server._heartbeat` to your own task manager.

        :return:
        `None`
        """
        if self.socket is not None:
            self.socket.bind((self.host, self.port))
            
            if self.serverType == ServerType.TCP:
                # TCP shenanigans that UDP does not fancy.
                self.socket.listen(self.maxConn)
                print(f"* Socket is now listening at {self.host}:{self.port}")

            self.status = ServerStatus.INIT

    def _heartbeat(self):
        """
        Server heartbeat/poll method.
        """
        while self.status == ServerStatus.INIT:
            if self.serverType == ServerType.UDP:
                self.udp_poll()
            else:
                self.tcp_poll()

    def heartbeat(self):
        """
        Call this function once to start server polling. Automatically called by [Server.connect]
        """
        thr = threading.Thread(target = self._heartbeat, args=())
        thr.start()

    def getFromIp(self, ip: str, port: int):
        """
        Get a client based on their IP and port. Returns `None` if no client is found.
        """
        for client in self.clients:
            if client.getIp() == ip and client.getPort() == port:
                return client

        return None

    def on_join_hook(self, func):
        """
        Hook a function to the event in which a client attempts to send a packet to this server.
        """
        self.onJoinListeners.append(func)

    def tcp_poll(self):
        """
        TCP socket polling method.
        """
        # Receive data from existing connections.
        for client in self.clients:
            data = client.conn.recv(BUFFER_SIZE)
            if not data:
                print(f"\t\t* [{client.ip}:{client.port}] did not send any data in return, indicating a disconnect.")
                client.close()
                self.clients.remove(client)
            
            self.on_recv(client, data)

        # Look out for new connections.
        conn, addr = self.socket.accept()
        client = Client(addr[0], addr[1], conn)
        print(f"\t* new connection has been established [{addr[0]}:{addr[1]}]")

        for func in self.onJoinListeners:
            func(client)

        self.clients.append(
            client
        )

    def udp_poll(self):
        """
        UDP socket polling method.
        """
        data, sender = self.socket.recvfrom(BUFFER_SIZE)

        self.on_recv(Client(sender[0], sender[1], None), data)
    
    def stop(self):
        """
        Stop the server by closing the socket.
        """
        print(f"* socket at {self.host}:{self.port} is now closing.")
        self.socket.close()

    def __del__(self):
        self.stop()