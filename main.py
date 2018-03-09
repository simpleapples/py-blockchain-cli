from cli.command import Command


def main():
    command = Command()

    command.start_peer('127.0.0.1', 5000)
    command.start_peer('127.0.0.1', 5001)

    import time
    time.sleep(1)

    command.connect_peer('127.0.0.1', 5000, '127.0.0.1', 5001)

    command.mine('127.0.0.1', 5000, 'hello')
    command.mine('127.0.0.1', 5001, 'world')

    command.get_chain('127.0.0.1', 5000)
    command.get_chain('127.0.0.1', 5001)


if __name__ == '__main__':
    main()
