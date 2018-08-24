import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port where the server is listening
server_address = ('localhost', 8341)
print('connecting to %s port %s' % server_address)
sock.connect(server_address)
try:
    
    # Send data
    
    is_active = True
    while is_active:
        message = input("please input something: ") + '\0'
        sock.sendall(message.encode('utf-8'))
        if 'quit' in message:
            is_active = False
        data = sock.recv(1024)
        print('received "%s"' % data, file=sys.stderr)

    # message = input("please input something: ") + '\0'
    # sock.sendall(message.encode('utf-8'))
    # data = sock.recv(1024)
    # print('received "%s"' % data, file=sys.stderr)

finally:
    print('closing socket')
    sock.close()

