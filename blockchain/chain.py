from blockchain.block import Block


class Chain(object):

    def __init__(self):
        genesis = Block(data='Welcome to blockchain cli!')
        self._chain_list = [genesis]
        self._difficulty = 4

    def mine(self, data):
        previous = self._latest_block
        nonce = 0
        while True:
            nonce += 1
            new = Block(previous.index + 1, nonce, previous.hash, data)
            if self._is_hash_valid(new.hash):
                self._chain_list.append(new)
                break

    def to_dict(self):
        return [item.to_dict() for item in self._chain_list]

    def _is_hash_valid(self, hash):
        return hash[:self._difficulty] == '0' * self._difficulty

    @property
    def _latest_block(self):
        return self._chain_list[-1]
