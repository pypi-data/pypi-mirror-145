"""
The server's view of what is a client; not the main client.
"""

from pydatanet.data import encode, decode

class Client:
    def __init__(self, ip: str, port: int, conn):
        self.ip = ip
        self.port = port
        self.conn = conn
    
    def close(self):
        return self.conn.close()

    def getIp(self):
        return self.ip

    def getPort(self):
        return self.port
    
    def _send(self, data: bytes):
        print(data)
        self.conn.send(data)

    def send(self, data: any):
        self._send(encode(data))