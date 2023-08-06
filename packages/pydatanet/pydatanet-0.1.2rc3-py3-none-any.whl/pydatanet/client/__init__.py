"""
The actual client that connects/sends data. Not the server representation.
"""

import socket
import enum
from socket import AF_INET, SO_REUSEADDR, SOCK_STREAM, SOCK_DGRAM, SOL_SOCKET
import threading

from pydatanet.data import encode, decode

BUFFER_SIZE = 2048

class ClientType(enum.Enum):
    TCP = 0
    UDP = 1

class ConnectStatus(enum.Enum):
    CONNECTED = 0
    DISCONNECTED = 1

class Client:
    def __init__(self, clientType = ClientType.TCP):
        self.clientType = clientType
        self.socket = None
        self.onRecvTCP = []
        self.onRecvUDP = []
        self.status = ConnectStatus.DISCONNECTED
        self.addr = ""
        self.port = 0

        if clientType == ClientType.TCP:
            self.socket = socket.socket(AF_INET, SOCK_STREAM)
        elif clientType == ClientType.UDP:
            self.socket = socket.socket(AF_INET, SOCK_DGRAM)
        else:
            raise ValueError(f"Invalid client type '{clientType}'!")

    def connect(self, address: str, port: int, autoPoll: bool = True):
        print(f"* connecting to [{address}:{port}]")
        if self.clientType == ClientType.TCP:
            self.socket.connect(
                (address, port)
            )

        self.addr = address
        self.port = port

        self.status = ConnectStatus.CONNECTED
        if autoPoll: self.heartbeat()
        print(f"\t* connected to [{address}:{port}]")

    def send(self, data: any):
        if self.clientType == ClientType.TCP:
            self.socket.send(encode(data))
        elif self.clientType == ClientType.UDP:
            self.socket.sendto(encode(data), (self.addr, self.port))

    def heartbeat(self):
        threading.Thread(target=self._heartbeatLoop, args=()).start()

    def _heartbeatLoop(self):
        while True:
            self._heartbeat()

    def _heartbeat(self):
        if self.status != ConnectStatus.CONNECTED:
            return
            
        if self.clientType == ClientType.TCP:
            self.poll_TCP()
        elif self.clientType == ClientType.UDP:
            self.poll_UDP()
        else:
            raise ValueError(self.clientType)

    def hook_tcp_recv(self, func):
        """
        Hook a function to the event in which a packet is received (TCP).
        """
        self.onRecvTCP.append(func)

    def hook_udp_recv(self, func):
        """
        Hook a function to the event in which a packet is received (TCP).
        """
        self.onRecvUDP.append(func)
    
    def poll_TCP(self):
        data = self.socket.recv(BUFFER_SIZE)
        if not data:
            print("\t* we have been disconnected from the server.")
            self.status = ConnectStatus.DISCONNECTED
            return
            
        data = decode(data)
        
        for event in self.onRecvTCP:
            event(data)

    def poll_UDP(self):
        data = self.socket.recvfrom(BUFFER_SIZE)
        data = decode(data)
        
        for event in self.onRecvUDP:
            event(data)