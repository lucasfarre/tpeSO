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

# retInit = cfunctions.serverInit("Test")

# up = True
# while up == True:
#     retConnect = cfunctions.serverConnect(retInit['socket_fd'])
#     print retConnect['json']
#     petition = fromJson(retConnect['json'])
#     id = petition['id']
#     if id == petitions['close']:
#         up = False
#     else:
#         if id == petitions['getAllFlights']:
#             petition = socketPackage(1, os.getpid(), serverback.getAllFlights(), petition['ip'],petition['port'])
#             #print (toJson(petition))
#             print str(retConnect['client_socket_fd'])
#             cfunctions.clientSend(retConnect['client_socket_fd'],toJson(petition))
# #    cfunctions.serverDisconnect(retConnect['client_socket_fd'])
# #    print(petition)
# cfunctions.serverDown(retInit['socket_fd'], retInit['socket_name'])

retInit = cfunctions.serverInit("Test")

up = True
while up == True:
    fd = cfunctions.serverConnect(retInit['socket_fd'])
    open = True
    while open:
        json = cfunctions.clientRecieve(fd)
        #json = os.read(fd, 1000)
        #o = fromJson(json)
        if json != None:
            print json
            petition = fromJson(json)
            id = petition['id']
            if id == petitions['getAllFlights']:
                p = socketPackage(1, os.getpid(), serverback.getAllFlights(), petition['ip'],petition['port'])
                cfunctions.clientSend(fd,toJson(p))
        #if 'id' in o:
        #    id = o['id']
        #if id == petitions['close']:
            #open = False
        #else:
            #if id == petitions['getAllFlights']:
                #print(json)
                #petition = socketPackage(1, os.getpid(), serverback.getAllFlights(), petition['ip'],petition['port'])
                #print (toJson(petition))
                #print str(retConnect['client_socket_fd'])
                #cfunctions.clientSend(fd,toJson(petition))
#    cfunctions.serverDisconnect(retConnect['client_socket_fd'])
#    print(petition)
cfunctions.serverDown(retInit['socket_fd'], retInit['socket_name'])