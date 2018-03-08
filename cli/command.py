import multiprocessing
import socket
import json

from blockchain.peer import Peer


class Command(object):

    def start_peer(self, host, port):
        p = multiprocessing.Process(target=self._start_peer, args=(host, port))
        p.start()

    def _start_peer(self, host, port):
        peer = Peer(host, port)
        peer.start()

    def mine(self, host, port, data):
        message = {'type': 'MINE', 'data': data}
        return self._dispatch_message_task(host, port, message)

    def get_chain(self, host, port):
        message = {'type': 'CHAIN'}
        return self._dispatch_message_task(host, port, message)

    def _dispatch_message_task(self, host, port, message):
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
        print('Type:', message['type'], 'Response:', response.decode('utf-8'))
        return response.decode('utf-8')
