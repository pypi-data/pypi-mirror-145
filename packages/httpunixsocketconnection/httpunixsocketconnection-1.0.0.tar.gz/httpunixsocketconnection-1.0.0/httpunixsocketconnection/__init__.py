import os.path
import socket
from http.client import HTTPConnection


class HTTPUnixSocketConnection(HTTPConnection):

    def __init__(self, unix_socket: str, timeout=None, blocksize=8192):
        super().__init__("localhost", timeout, blocksize)
        self.unix_socket = unix_socket

    def connect(self):
        if not os.path.exists(self.unix_socket):
            raise IOError(f"Socket {self.unix_socket} does not exist")

        self.sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.settimeout(self.timeout)
        self.sock.connect(self.unix_socket)
