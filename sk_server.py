import socket
from time import ctime

HOST = 'localhost'
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

while True:
    print('Server waiting for connection...')
    client_sock, addr = server_socket.accept()
    print('Client connected from: ', addr)
    while True:
        # socket is blocking here, i.e. recv()
        print('before recv...')
        data = client_sock.recv(BUFSIZ)
        print('after recv...')
        if not data or data.decode('utf-8') == 'END':
            break
        print("Received from client: %s" % data.decode('utf-8'))
        print("Sending the server time to client: %s" %ctime())
        try:
            client_sock.send(bytes(ctime(), 'utf-8'))
        except KeyboardInterrupt:
            print("Exited by user")
    client_sock.close()
server_socket.close()
    