import os
from classes import *
import cfunctions
from functions import *

print '\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n'

ip = raw_input('Ingrese el IP del servidor: ')
port = raw_input('Ingrese el puerto del servidor: ')
petition = socketPackage(1, os.getpid(), 'Petition Body', ip, int(port))

print str(len(toJson(petition)))

socket_fd = cfunctions.clientInit(ip,int(port))
s = ''
 
cfunctions.writen(socket_fd,toJson(petition), len(toJson(petition)))
last = 0
lastPackage = None
open = True
while open:
    json = cfunctions.readn(socket_fd, 77426)
    if json != None:
        print json[1]
        print 'bytes: ' + str(json[0])
        if json[0] == 77426:
            open = False
#         try:
#             petition = fromJson(json)
#         except ValueError:
#             print 'Paquete corrupto'
#             p = socketPackage(2, os.getpid(), None, petition['ip'],petition['port'])
#             lastPackage = p
#             cfunctions.clientSend(socket_fd,toJson(p))
#         else:
#             id = petition['id']
# #            if id == 0:
# #                open = False
#             if id == 1:
#                 print('Server Response: \n' + json)
#                 p = socketPackage(0, os.getpid(), None, petition['ip'],petition['port'])
#                 lastPackage = p
#                 cfunctions.clientSend(socket_fd,toJson(p))
#                 open = False
#             if id == 2:
#                 cfunctions.clientSend(socket_fd,toJson(lastPackage))
 
cfunctions.clientDown(socket_fd)