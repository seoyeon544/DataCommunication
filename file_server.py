import socket
import os

FLAGS = _ = None
DEBUG = False


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))

    files = {}

    for filename in os.listdir(FLAGS.directory):
        path = os.path.join(FLAGS.directory, filename)

        if os.path.isfile(path):
            files[filename] = {
                'path': path,
                'size': os.path.getsize(path)
            }

    print('Ready to file transfer')
    for filename in files:
        print(f'{filename} ({files[filename]}')

    print(f'Listening on {sock}')

    while True:
        data, client = sock.recvfrom(2 ** 16)
        data = data.decode('utf-8')
        print(f'Received {data} from {client}')

        cmd, _sep, filename = data.partition(' ')
        cmd = cmd.strip().upper()
        filename = filename.strip()

        if filename not in files:
            response = '404 Not Found'
            sock.sendto(response.encode('utf-8'), client)
            print(f'Send {response} to {client}')
            continue

        if cmd == 'INFO':
            response = str(files[filename]['size'])
            sock.sendto(response.encode('utf-8'), client)
            print(f'Send {response} to {client}')

        elif cmd == 'DOWNLOAD':
            path = files[filename]['path']

            with open(path, 'rb') as f:
                while True:
                    chunk = f.read(FLAGS.mtu)

                    if not chunk:
                        break

                    sock.sendto(chunk, client)

            print(f'Send {filename} to {client}')

        else:
            response = '400 Bad Request'
            sock.sendto(response.encode('utf-8'), client)
            print(f'Send {response} to {client}')


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser()

    parser.add_argument('--debug', action='store_true',
                        help='The present debug message')

    parser.add_argument('--address', type=str, default='0.0.0.0',
                        help='The address to serve service')

    parser.add_argument('--port', type=int, default=3034,
                        help='The port to serve service')

    parser.add_argument('--directory', type=str, default='files',
                        help='The directory containing files')

    parser.add_argument('--mtu', type=int, default=1500,
                        help='The maximum transfer size')

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug
    main()