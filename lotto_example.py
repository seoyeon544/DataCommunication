import socket
import random

FLAGS = _ = None
DEBUG = False


def generate_lotto(user_numbers):
    """사용자가 보낸 번호를 포함하여 6개의 로또 번호를 생성.

    요구사항:
      - user_numbers: 1~45 범위의 정수 리스트 (0~6개)
      - 사용자가 보낸 번호는 그대로 당첨 번호에 포함.
      - 부족한 개수만큼 1~45 가방에서 (이미 고른 번호는 제외)
        랜덤으로 추출.
      - 최종 6개를 오름차순으로 정렬하여 리스트로 반환.
      - 1~45 전체 집합:  set(range(1, 46))
      - 집합 차집합(A - B), random.choice(시퀀스) 를 활용.
    """
    # TODO: 1~45 가방에서 사용자가 고른 번호를 제외한 집합 생성.

    # TODO: 사용자가 고른 번호를 먼저 채택.

    # TODO: 6개가 될 때까지 가방에서 랜덤으로 하나씩 뽑아 추가.

    # TODO: 오름차순 정렬하여 반환.
    raise NotImplementedError('generate_lotto 를 구현하세요')


def parse_user_numbers(text):
    """클라이언트가 보낸 텍스트를 1~45 정수 리스트로 변환.

    요구사항:
      - 공백으로 구분된 숫자들을 정수로 변환.
      - 빈 입력이면 빈 리스트를 반환. (→ 서버가 전부 랜덤 생성)
      - 1~45 범위를 벗어나거나 숫자가 아닌 토큰은 무시.
      - text.split() 으로 공백 기준 분리
      - str.isdigit() 으로 숫자 여부 확인
    """
    # TODO: text 를 파싱하여 유효한 1~45 정수 리스트를 반환.
    raise NotImplementedError('parse_user_numbers 를 구현하세요')


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

        # TODO: text 를 파싱하고 로또 번호를 생성후,
        #       공백으로 구분된 문자열로 만들어 응답.
        #   1) parse_user_numbers(text) 로 입력 번호 추출
        #   2) generate_lotto(...) 로 6개 번호 생성
        #   3) ' '.join(...) 으로 문자열 변환
        #   4) sock.sendto(...) 로 client 에게 전송

        # (구현 후 아래 두 줄 형태로 응답 전송)
        # sock.sendto(response.encode('utf-8'), client)
        # print(f'Send {response} to {client}')


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