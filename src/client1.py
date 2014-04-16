import os
from classes import *
import cfunctions
from functions import *



ip = raw_input('Ingrese el IP del servidor: ')
port = raw_input('Ingrese el puerto del servidor: ')
petition = socketPackage(1, os.getpid(), 'Petition Body', ip, int(port))
socket_fd = cfunctions.clientInit(ip,int(port))
s = ''

cfunctions.clientSend(socket_fd,toJson(petition))
last = 0
lastPackage = None
open = True
while open:
    json = cfunctions.clientRecieve(socket_fd)
    if json != None:
        try:
            petition = fromJson(json)
        except ValueError:
            print 'Paquete corrupto'
            p = socketPackage(2, os.getpid(), None, petition['ip'],petition['port'])
            lastPackage = p
            cfunctions.clientSend(socket_fd,toJson(p))
        else:
            id = petition['id']
#            if id == 0:
#                open = False
            if id == 1:
                print('Server Response: \n' + json)
                p = socketPackage(0, os.getpid(), None, petition['ip'],petition['port'])
                lastPackage = p
                cfunctions.clientSend(socket_fd,toJson(p))
                open = False
            if id == 2:
                cfunctions.clientSend(socket_fd,toJson(p))

cfunctions.clientDown(socket_fd)    



