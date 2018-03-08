from blockchain.block import Block


class Chain(object):

    def __init__(self):
        genesis = Block(data='Welcome to blockchain cli!')
        self.chain_list = [genesis]
        self.difficulty = 3

    def mine(self, data):
        previous = self._latest_block
        nonce = 0
        while True:
            nonce += 1
            new = Block(previous.index + 1, nonce, previous.hash, data)
            if not self._is_hash_valid(new.hash):
                continue
            self.chain_list.append(new)

    def _is_hash_valid(self, hash):
        return hash[:self.difficulty] == '0' * self.difficulty

    @property
    def _latest_block(self):
        return self.chain_list[-1]
