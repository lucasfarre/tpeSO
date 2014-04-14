import os
from classes import *
import cfunctions
from functions import *

ip = raw_input('Ingrese el IP del servidor: ')
port = raw_input('Ingrese el puerto del servidor: ')
petition = socketPackage(1, os.getpid(), 'Petition Body', ip, int(port))
socket_fd = cfunctions.clientInit(ip,int(port))
print(toJson(petition))
cfunctions.clientSend(socket_fd,toJson(petition))

while True:
    data = cfunctions.clientRecieve(socket_fd,None)
    if data != None:
        print data