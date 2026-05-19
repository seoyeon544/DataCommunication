import socket

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(2)

    print(f'Ready to send using {sock}')

    while True:
        try:
            data = input('Data: ').strip()

            sock.sendto(data.encode('utf-8'),
                        (FLAGS.address, FLAGS.port))

            print(f'Request {data} to ({FLAGS.address}, {FLAGS.port})')

            with open(data.split()[-1], 'wb') as f:
                while True:
                    try:
                        data, server = sock.recvfrom(FLAGS.chunk_maxsize)
                    except socket.timeout:
                        break

                    f.write(data)

            print(f'File download success')

        except KeyboardInterrupt:
            print(f'\nShutting down... {sock}')
            break

    sock.close()


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug',
                        action='store_true',
                        help='The present debug message')

    parser.add_argument('--address',
                        type=str,
                        required=True,
                        help='The address to send data')

    parser.add_argument('--port',
                        type=int,
                        required=True,
                        help='The port to send data')

    parser.add_argument('--chunk_maxsize',
                        type=int,
                        default=1500,
                        help='The maximum size of received chunk')

    FLAGS, _ = parser.parse_known_args()

    DEBUG = FLAGS.debug

    main()