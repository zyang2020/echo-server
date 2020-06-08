import socket
import sys
import traceback


def client(msg, log_buffer=sys.stderr):
    HOST = '127.0.0.1'
    PORT = 51000

    # create a client side socket
    print('creating a client side socket')
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print('connecting to {0} port {1}'.format(HOST, PORT), file=log_buffer)
    # connect client socket to the server.
    sock.connect((HOST, PORT))

    # you can use this variable to accumulate the entire message received back
    # from the server
    received_message = ''

    # this try/finally block exists purely to allow us to close the socket
    # when we are finished with it
    try:
        print('sending "{0}"'.format(msg), file=log_buffer)
        # TODO: send your message to the server here.
        sock.sendall(msg.encode('utf8'))
        # TODO: the server should be sending you back your message as a series
        #       of 16-byte chunks. Accumulate the chunks you get to build the
        #       entire reply from the server. Make sure that you have received
        #       the entire message and then you can break the loop.
        #
        #       Log each chunk you receive.  Use the print statement below to
        #       do it. This will help in debugging problems
        chunk = ''
        while True:
            chunk = sock.recv(16)
            if len(chunk) < 16:
                print('received "{0}"'.format(chunk.decode('utf8')),
                      file=log_buffer)
                received_message += chunk.decode('utf8')
                break
            print('received "{0}"'.format(chunk.decode('utf8')),
                  file=log_buffer)
            received_message += chunk.decode('utf8')
    except Exception as e:
        traceback.print_exc()
        sys.exit(1)
    finally:
        # TODO: after you break out of the loop receiving echoed chunks from
        #       the server you will want to close your client socket.
        print('closing socket', file=log_buffer)
        sock.close()
        # TODO: when all is said and done, you should return the entire reply
        # you received from the server as the return value of this function.
        return received_message


def list_services(begin, end):
    if begin == end or begin > end:
        print('port range error (0-65535)!')
        sys.exit(1)
    if begin < 0 or end > 65535:
        print('Out of the port range (0-65535)!')
        sys.exit(1)

    tot = 0
    for i in range(begin, end + 1):
        try:
            service = socket.getservbyport(i)
            print(f'--- {service} service are provided at port:{i} ---')
            tot += 1
        except OSError:
            pass
            #print(f'No Service provided at port:{i}')
    return tot

if __name__ == '__main__':
    if len(sys.argv) != 2:
        usage = '\nusage: python echo_client.py "this is my message"\n'
        print(usage, file=sys.stderr)
        sys.exit(1)

    msg = sys.argv[1]
    received_msg = client(msg)
    print(f'\n Received Message \n "{received_msg}"')
