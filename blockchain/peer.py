import json
import socketserver

from blockchain.chain import Chain


class _RequestHandler(socketserver.BaseRequestHandler):

    def handle(self):
        message_str = self.request.recv(1024).strip().decode('utf-8')
        message_obj = json.loads(message_str)
        message_type = message_obj['type']
        response = 'OK'
        peer = self.server.peer
        if message_type == 'MINE':
            peer.mine(message_obj['data'])
        elif message_type == 'CONNECT':
            host = message_obj['host']
            port = message_obj['port']
            peer.connect_to_peer(host, port)
        elif message_type == 'CHAIN':
            response = json.dumps(peer.chain.to_dict())
        self.request.sendall(response.encode('utf-8'))


class Peer(object):

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self.peers = set()
        self.chain = Chain()

    def start(self):
        handler = _RequestHandler
        handler.chain = self.chain
        server = socketserver.ThreadingTCPServer(
            (self.host, self.port), _RequestHandler)
        server.peer = self
        server.serve_forever()
        print(f'Peer running at {self.host}:{self.port}')

    def connect_to_peer(self, host, port):
        if (host, port) in self.peers:
            return
        self.peers.add((host, port))

    def disconnect_from_peer(self, host, port):
        if (host, port) not in self.peers:
            return
        self.peers.remove((host, port))

    def mine(self, data):
        return self.chain.mine(data)
