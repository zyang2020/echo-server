import select
import queue
import socket
import sys
import traceback


def server(log_buffer=sys.stderr):

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.setblocking(0) # set '0' means non-blocking socket

    # bind the socket to the port
    server_address = ('127.0.0.1', 51000)
    server_socket.bind(server_address)
    print('startng up on {} port:{}'.format(*server_address), file=log_buffer)
    # listen for incoming connections
    server_socket.listen(5)

    try:
        # select() has three arguments.
        # The first is a list of the socket objects
        # that to be checked for incoming data to be read.
        # right now, we know we have a input socket "server_socket" for sure.
        inputs = [server_socket]

        # The second is a list of socket objects that will receive outgoing
        # data. Right now, we don't know any outgoing socket yet.
        outputs = []
        # connection sockets are added to and removed from above lists latter.

        # since we are using non-blocking server socket, so the server socket
        # will wait for a socket to become writable before sending any data, so
        # each output socket need a queue to store the output data.
        # we are using a dictionary to store the message related to each socket
        # object.
        message_queues = {}

        # main looop
        while inputs:
            print("Waiting for the event", file=log_buffer)
            readable, writable, error = select.select(inputs, outputs, inputs)

            # all the sockets in the 'readable' list have incoming data buffered
            # and available to be read.
            for sock in readable:
                # if the socket is the 'server_socket' listening  socket, then
                # it means it is ready to accept incoming connection.
                if sock is server_socket:
                    connection, client_address = sock.accept()
                    print('new connection from {}'.format(client_address),
                          file=log_buffer)
                    # set the client socket a non-blocking socket
                    connection.setblocking(0)
                    # add the client socket to the input socket list.
                    inputs.append(connection)

                    # give the client-side socket a queue to store the echo msg.
                    message_queues[connection] = queue.Queue()
                # if the socket is a client-side socket.
                else:
                    data = sock.recv(16) # read in data
                    if data: # if client socket has data
                        print('Server received {} from {}'.
                              format(data, sock.getpeername()),
                              file=log_buffer)
                        message_queues[sock].put(data)
                        # add the socket to the output list for echo.
                        if sock not in outputs:
                            outputs.append(sock)
                    else: # if the client socket didn't send in any data
                        #print('Server remove socket {} from input check list.'
                        #      .format(client_address), file=log_buffer)
                        inputs.remove(sock)

            # all the sockets in the 'writable' list have free space in their
            # buffer and are ready to be written to.
            for sock in writable:
                try:
                    msg = message_queues[sock].get_nowait()
                except queue.Empty:
                    # print('output queue for socket {} is empty.'.
                    #       format(sock.getpeername()), file=log_buffer)
                    # don't need to check this socket for output again.
                    if sock in outputs:
                        outputs.remove(sock)
                    print('Server closing client socket {}'
                          .format(sock.getpeername()), file=log_buffer)
                    sock.close()
                else:
                    print(f'Server sending {msg} to '
                          f'client socket {sock.getpeername()}')
                    sock.send(msg)

            # if there is error in error list, then the socket is closed.
            for sock in error:
                print(f' handing error for :{stock.getpeername()}')
                inputs.remove(sock)
                if sock in outputs:
                    outputs.remove(sock)
                sock.close()

    except KeyboardInterrupt:
        # TODO: Use the python KeyboardInterrupt exception as a signal to
        #       close the server socket and exit from the server function.
        #       Replace the call to `pass` below, which is only there to
        #       prevent syntax problems
        server_socket.close()
        print('quitting echo server', file=log_buffer)

if __name__ == '__main__':
    server()
    sys.exit(0)
