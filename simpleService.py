import win32service  
import win32serviceutil  
import win32event  
import socket
import sys
import servicemanager  
  
class PySvc(win32serviceutil.ServiceFramework):  
    # you can NET START/STOP the service by the following name  
    _svc_name_ = "PySvc"  
    # this text shows up as the service name in the Service  
    # Control Manager (SCM)  
    _svc_display_name_ = "Python Test Service"  
    # this text shows up as the description in the SCM  
    _svc_description_ = "This service writes stuff to a file"  
      
    def __init__(self, args):  
        win32serviceutil.ServiceFramework.__init__(self,args)  
        # create an event to listen for stop requests on  
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)  
      
    # core logic of the service     
    def SvcDoRun(self):  
          
        rc = None  
          
        myServer(self.hWaitStop)

        # # if the stop event hasn't been fired keep looping  
        # while rc != win32event.WAIT_OBJECT_0:  
        #     with open(r'c:\a\service_test.log', 'a+') as f:
        #         f.write('save data\n')
        #         f.write("rc = {}\n".format(rc))
        #         f.flush()  
        #     # block for 5 seconds and listen for a stop event  
        #     rc = win32event.WaitForSingleObject(self.hWaitStop, 10000)  

        # with open(r'c:\a\service_test.log', 'a+') as f:
        #     f.write("after rc = {}\n".format(rc))
      
    # called when we're being shut down      
    def SvcStop(self):  
        # tell the SCM we're shutting down  
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)  
        # fire the stop event  
        with open(r'c:\a\service_test.log', 'a+') as f:
            f.write("set event first?\n")
        win32event.SetEvent(self.hWaitStop)  
          
def myServer(hWaitStop):
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8341 # Arbitrary non-privileged port
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # if timeout is set to 10.0, then after 10s, the while 1 loop will exit
    # s.settimeout(10.0)
    print('Socket created')
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
         
        print('Socket bind complete')
         
        #Start listening on socket
        s.listen(10)
        print('Socket now listening')
         
        #now keep talking with the client
        rc = None
        # while 1:
        while rc != win32event.WAIT_OBJECT_0:   
            #wait to accept a connection - blocking call
            connection, client_address= s.accept()
            print('Connected with ' + client_address[0] + ':' + str(client_address[1]))

            with open(r'c:\a\x.log', 'a+') as f:
                f.write('rc = {}\n'.format(rc))
            try:
                # print(>>sys.stderr, 'connection from', client_address)

                # Receive the data in small chunks and retransmit it
                # while True:
                while True:   
                    data = connection.recv(1024)
                    # print >>sys.stderr, 'received "%s"' % data
                    if data:
                        print('sending data back to the client')
                        connection.sendall(data)
                    else:
                        print('no more data from {}'.format(client_address))
                        with open(r'c:\a\x.log', 'a+') as f:
                            f.write('no more data...break\n')
                        break

            except Exception as e:
                with open(r'c:\a\x.log', 'a+') as f:
                    f.write(str(e) + '\n')
                    
            finally:
                # Clean up the connection
                with open(r'c:\a\x.log', 'a+') as f:
                    f.write('close connection\n')
                connection.close()
                rc = win32event.WaitForSingleObject(hWaitStop, 1000) 
    except socket.timeout:
        with open(r'c:\a\x.log', 'a+') as f:
            f.write('time out\n')
    except socket.error as msg:
        with open(r'c:\a\x.log', 'a+') as f:
            f.write('Error Code : ' + str(msg[0]) + ' Message ' + msg[1] + '\n')
        sys.exit()

def pureServer():
    count = 0
    HOST = ''   # Symbolic name, meaning all available interfaces
    PORT = 8341 # Arbitrary non-privileged port
     
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # if timeout is set to 10.0, then after 10s, the while 1 loop will exit
    # s.settimeout(10.0)
    print('Socket created')
     
    #Bind socket to local host and port
    try:
        s.bind((HOST, PORT))
         
        print('Socket bind complete')
         
        #Start listening on socket
        s.listen(1)
        print('Socket now listening')
         
        #now keep talking with the client
        while 1:
            #wait to accept a connection 
            connection, client_address= s.accept()
            print('Connected with ' + client_address[0] + ':' + str(client_address[1]))
            try:

                # Receive the data in small chunks and retransmit it
                while True:   
                    # socket is blocking here!!!
                    data = connection.recv(10).decode()
                    while '\0' not in data:
                        data += connection.recv(10).decode()

                    # need to test if 'quit' in data first, ow, it will go to elif data block, and won't break the inner
                    # while loop, and won't close the socket
                    # if the socket is not closed, then client can't start a new socket, because the current one is
                    # still not closed yet

                    if not data :
                        print('no data is coming')
                        break
                    # if 'quit' in data:
                    #     print('received quit request from client')
                    #     break
                    try:
                        print('got data {}, and sending data back to the client'.format(data.rstrip('\0')))
                        connection.sendall(str(count).encode('utf-8'))
                        count += 1
                    except KeyboardInterrupt:
                        print("Exited by user")

            except Exception as e:
                print(e)
                raise
                    
            finally:
                # Clean up the connection
                print('close connection\n')
                connection.close()
        s.close()
    except socket.timeout:
        print('time out\n')
        # time out is thrown by accept(), raise will tell you it is accept()
        raise
    except socket.error as msg:
        print('error code {}'.format(msg[0]))
        sys.exit()

        

if __name__ == '__main__':  
    win32serviceutil.HandleCommandLine(PySvc)  
    # myServer( win32event.CreateEvent(None, 0, 0, None))
    # pureServer()
