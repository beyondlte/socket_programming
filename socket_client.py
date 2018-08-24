# note: py3!!!
import socket

HOST = 'localhost'
PORT = 12345

def prep_msg(msg):
    msg += '\0'
    print('prepare msg {}'.format(msg))
    return msg.encode()

def send_msg(sock, msg):
    data = prep_msg(msg)
    sock.sendall(data)

def recv_msg(sock):
    try:
        data = bytearray()
        msg = ''
        while not msg:
            recvd = sock.recv(16)
            if not recvd:
                raise 
            data = data + recvd
            if b'\0' in recvd:
                msg = data.rstrip(b'\0')
        msg = msg.decode()
    except Exception as e:
        print(e)
        raise

    return msg

def create_client_socket(host, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host,port))
    print('\nConnected to {}:{}'.format(HOST,PORT))
    return sock

def run_socket(host, port):
    while True:
        try:
            client_socket = create_client_socket(HOST, PORT)
            print("Type message, enter to send, 'q' to quit")
            msg = input()
            print('msg = {}'.format(msg))
            if msg == 'q':
                break
            send_msg(client_socket, msg)
            print('Sent message: {}'.format(msg))
            msg = recv_msg(client_socket)
            print('Received echo: ' + msg)
        except Exception as e:
            print('Socket error: {}'.format(e))
            break
        finally:
            client_socket.close()
            print('Closed connection to server\n')

if __name__ == '__main__':
    run_socket(HOST, PORT)

