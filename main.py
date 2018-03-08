from cli.command import Command


def main():
    command = Command()
    command.start_peer('127.0.0.1', 5000)
    command.mine('127.0.0.1', 5000, 'hello')
    command.get_chain('127.0.0.1', 5000)


if __name__ == '__main__':
    main()
