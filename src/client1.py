import os
from classes import *
import cfunctions
from functions import *

ip = raw_input('Ingrese el IP del servidor: ')
port = raw_input('Ingrese el puerto del servidor: ')
petition = socketPackage(1, os.getpid(), 'Petition Body', ip, int(port))
socket_fd = cfunctions.clientInit(ip,int(port))
s = ''
while s != 'quit':
    cfunctions.clientSend(socket_fd,toJson(petition))
    open = True
    while open:
        json = cfunctions.clientRecieve(socket_fd)
        if json != None:
            try:
                petition = fromJson(json)
            except ValueError:
                print 'Paquete corrupto'
                p = socketPackage(2, os.getpid(), None, petition['ip'],petition['port'])
                cfunctions.clientSend(socket_fd,toJson(p))
            else:          
                print('Server Response: \n' + json)
                open = False
    s = raw_input('enter to resend, "quit" to exit: ')
    



