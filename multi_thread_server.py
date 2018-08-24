import threading
import socket_server

HOST = socket_server.HOST
PORT = socket_server.PORT 

def handle_client(sock, addr):
    """ Receive one message and echo it back to client, then close
    socket """
    try:
        msg = socket_server.recv_msg(sock) # blocks until received
        # complete message
        msg = '{}: {}'.format(addr, msg)
        print(msg)
        socket_server.send_msg(sock, msg) # blocks until sent

    except (ConnectionError, BrokenPipeError):
        print('Socket error')

    finally:
        print('Closed connection to {}'.format(addr))
        sock.close()

if __name__ == '__main__':
    listen_sock = socket_server.create_listen_socket(HOST, PORT)
    addr = listen_sock.getsockname()
    print('Listening on {}'.format(addr))

    try:
        while True:
            client_sock, addr = listen_sock.accept()
            # Thread will run function handle_client() autonomously
            # and concurrently to this while loop
            # daemon=True, means we can Ctrl+c to exit without exiting all threads
            # if daemon=False, then ctrl+c not working, have to use ctrl+break
            thread = threading.Thread(target=handle_client, args=[client_sock, addr], daemon=True)
            thread.start()
            print('Connection from {}'.format(addr))
    except Exception as e:
        print('Error: {}'.format(e))


