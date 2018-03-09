import json
import socket
import socketserver
import multiprocessing

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
        elif message_type == 'DISCONNECT':
            host = message_obj['host']
            port = message_obj['port']
            peer.disconnect_from_peer(host, port)
        elif message_type == 'GET_CHAIN':
            response = json.dumps(peer.chain.to_dict())
        elif message_type == 'BROADCAST_CHAIN':
            chain = message_obj['chain']
            peer.replace_chain(chain)
        self.request.sendall(response.encode('utf-8'))


class Peer(object):

    def __init__(self, host='127.0.0.1', port=5000):
        self.host = host
        self.port = port
        self._peers = set()
        self._chain = Chain()

    def start(self):
        handler = _RequestHandler
        handler.chain = self._chain
        server = socketserver.ThreadingTCPServer(
            (self.host, self.port), _RequestHandler)
        server.peer = self
        try:
            server.serve_forever()
            print(f'Peer running at {self.host}:{self.port}')
        except KeyboardInterrupt as _:
            server.server_close()
            print(f'Peer closed at {self.host}:{self.port}')

    def connect_to_peer(self, host, port):
        if (host, port) in self._peers:
            return
        self._peers.add((host, port))
        self._send_connect_message(host, port)

    def disconnect_from_peer(self, host, port):
        if (host, port) not in self._peers:
            return
        self._peers.remove((host, port))

    def mine(self, data):
        self.chain.mine(data)
        self._broadcast_chain()

    def replace_chain(self, chain):
        self._chain.replace_chain(chain)

    @property
    def chain(self):
        return self._chain

    def _broadcast_chain(self):
        pool = multiprocessing.Pool(5)
        results = []
        message = {'type': 'BROADCAST_CHAIN', 'chain': self._chain.to_dict()}
        for (host, port) in self._peers:
            results.append(pool.apply_async(
                self._send_message, args=(host, port, message)))
        pool.close()
        pool.join()

    def _send_connect_message(self, host, port):
        message = {'type': 'CONNECT', 'host': self.host, 'port': self.port}
        self._unicast(host, port, message)

    def _unicast(self, host, port, message):
        pool = multiprocessing.Pool(1)
        result = pool.apply_async(
            self._send_message, args=(host, port, message))
        pool.close()
        pool.join()
        return result.get()

    def _broadcast(self, message):
        pool = multiprocessing.Pool(5)
        for (host, port) in self._peers:
            result = pool.apply_async(
                self._send_message, args=(host, port, message))
        pool.close()
        pool.join()

    def _send_message(self, host, port, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(json.dumps(message).encode('utf-8'))
        response = s.recv(1024, 0)
        s.close()
        print('Type:', message['type'], 'Response:',
              response.decode('utf-8'))
        return response.decode('utf-8')
