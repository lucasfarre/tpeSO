import socket
import cfunctions
import os
from functions import fromJson
import string

print('SRV Server 1.0')
print('Server running...')
print(socket.gethostbyname(socket.gethostname()))

retInit = cfunctions.serverInit("Test")

up = True
while up == True:
    retConnect = cfunctions.serverConnect(retInit['socket_fd'])
    petition = fromJson(retConnect['json'])
    if petition['id'] == 0:
        up = False
    cfunctions.serverDisconnect(retConnect['client_socket_fd'])
    print(petition)
cfunctions.serverDown(retInit['socket_fd'], retInit['socket_name'])