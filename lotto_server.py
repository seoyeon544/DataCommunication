import socket
import random

FLAGS = _ = None
DEBUG = False


def generate_lotto(user_numbers):
    lotto = list(user_numbers)

    # 1~45 중 이미 선택된 번호 제외
    bag = list(set(range(1, 46)) - set(lotto))
    bag.sort()

    print(f'Numbers in bag: {bag}')

    while len(lotto) < 6:
        selected = random.choice(bag)
        print(f'Selected: {selected}')

        lotto.append(selected)
        bag.remove(selected)

    return sorted(lotto)


def parse_user_numbers(text):
    numbers = []

    for token in text.split():
        if token.isdigit():
            num = int(token)

            if 1 <= num <= 45 and num not in numbers:
                numbers.append(num)

            if len(numbers) == 6:
                break

    return numbers


def main():
    if DEBUG:
        print(f'Parsed arguments {FLAGS}')
        print(f'Unparsed arguments {_}')

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((FLAGS.address, FLAGS.port))

    print(f'Listening on {sock}')

    while True:
        data, client = sock.recvfrom(2 ** 16)
        text = data.decode('utf-8')

        print(f'Received {text} from {client}')

        user_numbers = parse_user_numbers(text)
        lotto_numbers = generate_lotto(user_numbers)

        response = ' '.join(map(str, lotto_numbers))

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

    FLAGS, _ = parser.parse_known_args()
    DEBUG = FLAGS.debug

    main()