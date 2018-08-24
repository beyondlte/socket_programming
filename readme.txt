python simpleService.py install
net start PySvc

python echoClient.py will talk to the service
quit to stop client

net stop PySvc
needs to call python echoClient.py at the same time
