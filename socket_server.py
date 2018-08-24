# note: py3!!!
import socket
import sys
import traceback
HOST = 'localhost'
PORT = 12345

def create_listen_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind((host, port))
    sock.listen(10)
    return sock

def recv_msg(sock):
    data = bytearray()
    msg = ''
    try:
        while not msg:
            print('blocking at recv before')
            # socket is blocking here, but sock.recv() is not called yet, so recvd is not assigned yet
            # if we ctrl+c on client, then here we'll catch a connection was forcibly closed exception
            # if we don't catch here, then this exception is not visible
            recvd = sock.recv(16)
            print('after recv')
            if not recvd:
                # when client closes the socket, then the socket is not blocking at recv() anymore,
                # and then recv() will return nothing, so we will have recvd to be None
                print('nothing received')
                break 
            # here we continuely receive data from client, until we get '\0'
            data = data + recvd
            if b'\0' in recvd:
                msg = data.rstrip(b'\0')
        if msg != '':
            msg = msg.decode('utf-8')
    except Exception as e:
        print('Socket error: {}'.format(e))
        traceback.print_exc(file=sys.stdout)
    return msg

def prep_msg(msg):
    msg += '\0'
    return msg.encode()

def send_msg(sock, msg):
    try:
        data = prep_msg(msg)
        sock.sendall(data)
    except Exception as e:
        print('Socket send error: {}'.format(e))

def handle_client(sock, addr):
    try:
        msg = recv_msg(sock)
        print('{}: {}'.format(addr, msg))
        send_msg(sock, msg)
    except Exception as e:
        print('Socket error: {}'.format(e))
    finally:
        print('Closed connection to {}'.format(addr))
        sock.close()

def run_socket(host, port):
    listen_sock = create_listen_socket(host, port)
    addr = listen_sock.getsockname()
    print('listening on {}'.format(addr))

    while True:
        client_sock, addr = listen_sock.accept()
        print('connection from {}'.format(addr))
        handle_client(client_sock, addr)

if __name__ == '__main__':
    run_socket(HOST, PORT)

