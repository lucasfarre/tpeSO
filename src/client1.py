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
        data = cfunctions.clientRecieve(socket_fd)
        if data != None:
            print('Server Response: \n' + data)
            open = False
    s = raw_input('enter to resend, "quit" to exit: ')
    



