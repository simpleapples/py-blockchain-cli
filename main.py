from blockchain.peer import Peer


def run_peer_1():
    peer = Peer('127.0.0.1', 5000)
    peer.start()


def run_peer_2():
    peer = Peer('127.0.0.1', 5001)
    peer.start()
    peer.connect_to_peer('127.0.0.1', 5000)
    peer.boardcast('hhhhhhhh'.encode('utf-8'))
    peer.boardcast('aaaaa'.encode('utf-8'))


def main():
    # run_peer_1()
    run_peer_2()


if __name__ == '__main__':
    main()
