import unittest

from blockchain.block import Block


class TestBlock(unittest.TestCase):

    def test_genesis_block(self):
        genesis = Block(
            0, 0, '0', 'Welcome to blockchain cli!',
            '8724f78170aee146b794ca6ad451d23c254717727e18e2b9643b81d5666aa908',
            1520572079.336289)
        self.assertEqual(genesis, Block.genesis())

    def test_hash_generate(self):
        block = Block(
            index=1, nonce=80578,
            previous_hash=(
                '8724f78170aee146b794ca6ad451d23c254717727e18e2b9643b81d5666aa'
                '908'),
            data='hello',
            timestamp=1520923121.335219)
        self.assertEqual(
            block.hash,
            '0000f307ce360b39986cc164b7770f3029acd8f568be13765b22b482981675ca')

    def test_to_dict(self):
        block = Block(
            0, 0, '0', 'Welcome to blockchain cli!',
            '8724f78170aee146b794ca6ad451d23c254717727e18e2b9643b81d5666aa908',
            1520572079.336289)
        block_dict = {
            'index': 0,
            'previous_hash': '0',
            'timestamp': 1520572079.336289,
            'data': 'Welcome to blockchain cli!',
            'nonce': 0,
            'hash': (
                '8724f78170aee146b794ca6ad451d23c254717727e18e2b9643b81d5666aa'
                '908')
        }
        self.assertEqual(block.to_dict(), block_dict)
