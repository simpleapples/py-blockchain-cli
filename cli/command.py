import multiprocessing
import socket
import json

from blockchain.peer import Peer


class Command(object):

    def start_peer(self, host, port):
        p = multiprocessing.Process(target=self._start_peer, args=(host, port))
        p.start()
        print(f'Peer running at {host}:{port}')

    def _start_peer(self, host, port):
        peer = Peer(host, port)
        peer.start()

    def connect_peer(self, host, port, target_host, target_port):
        message = {'type': 'CONNECT', 'host': target_host, 'port': target_port}
        result = self._unicast(host, port, message)
        if result == 'OK':
            print(f'Peer {host}:{port} connected to {target_host}:{target_port}')
        else:
            print('Connect failed')
        return result

    def mine(self, host, port, data):
        print('Mining...')
        message = {'type': 'MINE', 'data': data}
        result = self._unicast(host, port, message)
        if result == 'OK':
            print('A new block was mined')
        else:
            print('Mine failed')
        return result

    def get_chain(self, host, port):
        message = {'type': 'SHOW'}
        result = self._unicast(host, port, message)
        if result:
            print(result)
        else:
            print('Empty blockchain')
        return result

    def _unicast(self, host, port, message):
        pool = multiprocessing.Pool(1)
        result = pool.apply_async(
            self._send_message, args=(host, port, message))
        pool.close()
        pool.join()
        return result.get()

    def _send_message(self, host, port, message):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((host, port))
        s.send(json.dumps(message).encode('utf-8'))
        response = s.recv(1024, 0)
        s.close()
        return response.decode('utf-8')
