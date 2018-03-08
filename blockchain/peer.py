import socket
import json

from blockchain.chain import Chain


class Peer(object):

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.peers = set()
        self.chain = Chain()

    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((self.host, self.port))
        s.listen(5)
        try:
            print(f'Peer running at {self.host}:{self.port}')
            while True:
                conn, _ = s.accept()
                message = conn.recv(1024)
                print(message)
                self._handle_message(message)
        except KeyboardInterrupt as _:
            pass
        finally:
            s.close()
            print(f'Peer closed at {self.host}:{self.port}')

    def connect_to_peer(self, host, port):
        if (host, port) in self.peers:
            return
        self.peers.add((host, port))

    def disconnect_from_peer(self, host, port):
        if (host, port) not in self.peers:
            return
        self.peers.remove((host, port))

    def mine(self):
        pass

    # TODO: should be private method
    def boardcast(self, message):
        for (host, port) in self.peers:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((host, port))
            s.sendall(message)
            s.close()

    def _handle_message(self, message):
        print(message)
        return ''
