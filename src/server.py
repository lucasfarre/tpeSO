import socket
import cfunctions
import os
from functions import fromJson, toJson
import string
import serverback
from classes import *

petitions = {'close':0, 'getAllFlights':1}
print('SRV Server 1.0')
print('Server running...')
ip = socket.gethostbyname(socket.gethostname())
print(ip)

retInit = cfunctions.serverInit("Test")

up = True
while up == True:
    retConnect = cfunctions.serverConnect(retInit['socket_fd'])
    petition = fromJson(retConnect['json'])
    id = petition['id']
    if id == petitions['close']:
        up = False
    else:
        if id == petitions['getAllFlights']:
            petition = socketPackage(1, os.getpid(), serverback.getAllFlights(), petition['ip'],petition['port'])
            print (toJson(petition))
            cfunctions.sendPetition(1, os.getpid(), toJson(petition),petition['ip'],petition['port'])
    cfunctions.serverDisconnect(retConnect['client_socket_fd'])
#    print(petition)
cfunctions.serverDown(retInit['socket_fd'], retInit['socket_name'])