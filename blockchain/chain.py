from blockchain.block import Block


class Chain(object):

    def __init__(self):
        genesis = Block.genesis()
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

    def replace_chain(self, chain):
        if len(chain) > len(self._chain_list):
            chain_list = []
            for block in chain:
                chain_list.append(Block(
                    int(block['index']), int(block['nonce']),
                    block['previous_hash'], block['data'], block['hash'],
                    float(block['timestamp'])))
            self._chain_list = chain_list

    def to_dict(self):
        return [item.to_dict() for item in self._chain_list]

    def _is_hash_valid(self, hash):
        return hash[:self._difficulty] == '0' * self._difficulty

    @property
    def _latest_block(self):
        return self._chain_list[-1]
