import time
from hashlib import sha256


class Block(object):

    def __init__(self, index=0, nonce=0, previous_hash='0', data=''):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time.time()
        self.data = data
        self.nonce = nonce
        self.hash = self._calculate_hash()

    def _calculate_hash(self):
        original_str = ''.join([
            str(self.index), self.previous_hash, str(self.timestamp), self.data,
            str(self.nonce)])
        return sha256(original_str.encode('utf-8')).hexdigest()

    def to_dict(self):
        return {
            'index': str(self.index),
            'previous_hash': self.previous_hash,
            'timestamp': self.timestamp,
            'data': self.data,
            'nonce': self.nonce,
            'hash': self.hash
        }
