# -'- coding: iso8859-1 -'-

import os
from cfunctions import *
from functions import *
from dbback import *

####################################################################################################
##### SRV Signal Server v2.0
##### Ejercicio 2.a.1
####################################################################################################

transitionFileName = '.pet.srv'

def serverInit():
    petitionfd = open(transitionFileName,'w')
    petitionfd.seek(0)
    petitionfd.truncate()
    petitionfd.write(str(os.getpid()))
    petitionfd.flush()
    os.fsync(petitionfd.fileno())
    petitionfd.close()    
    
def getClientPID(petition):
    return int(petition['pid'])

print('Server: Files & Signals')
while True:
    serverInit()
    print('Esperando recibir una se�al')
    recieveSignal()
    fd = open(transitionFileName,'r+')
    petition = fd.read()
    petition = fromJson(petition)
    clientPID = getClientPID(petition)
    print('Petici�n recibida:')
    print toPrettyJson(petition)
    if petition['id'] == 1:
        reWrite(fd,toJson(getAllFlights()))
        fd.close()
        sendSignal(clientPID)
        recieveSignal()
    if petition['id'] == 2:
        checkIn(petition['data'],petition['passenger'],petition['seat'])
        sendSignal(clientPID)
    if petition['id'] == 3:
        addFlight(petition['data'])
        sendSignal(clientPID)
    if petition['id'] == 4: 
        removeFlight(petition['data'])
        sendSignal(clientPID)
    
    
    
    
