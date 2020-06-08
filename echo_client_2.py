import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    server_address = ('127.0.0.1', 51000)

    # create two client side sockets
    socks = [socket.socket(socket.AF_INET, socket.SOCK_STREAM),
             socket.socket(socket.AF_INET, socket.SOCK_STREAM)
             ]
    print('Client connecting to {} port {}'
          .format(*server_address), file=log_buffer)
    for s in socks:
        s.connect(server_address)

    # two socket send the same msg.
    for s in socks:
        print('Client sending "{}" to socket:{}'.format(s.getsockname(), msg),
              file=log_buffer)
        s.send(msg.encode('utf8'))

    # check the responses.
    for s in socks:
        tmp_msg = ''
        while True:
            chunk = s.recv(16)
            if len(chunk) < 16:
                tmp_msg += chunk.decode('utf8')
                print('Client received "{}" from socket:{}'.format(tmp_msg,
                      s.getsockname()), file=log_buffer)
                s.close()
                break
            tmp_msg += chunk.decode('utf8')
    return tmp_msg

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    client(msg)
