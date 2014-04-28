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

#TODO Falta poner un lock bloqueante porque sino se pisan los checkins!!!.
#HAY QUE BLOQUEAR LA BASE DE DATOS CADA VEZ QUE UN CLIENTE LA ESTÁ USANDO. ES LO MÁS FACIL
#SINO HAY QUE CONTEMPLAR MUCHOS CASOS. CON EL LOCK BLOQUEANTE EL CLIENTE SE QUEDA ESPERANDO
#AUTOMATICAMENTE HASTA QUE EL ARCHIVO SE DESBLOQUEE!!!

#TODO Acá el servidor no catchea el Ctrl-C porque se queda colgado en C hasta que recibe alguna señal
#¿como arreglamos eso?

print('Server: Files & Signals')
while True:
    serverInit()
    print('Esperando recibir una señal')
    recieveSignal()
    fd = open(transitionFileName,'r+')
    petition = fd.read()
    petition = fromJson(petition)
    clientPID = getClientPID(petition)
    print('Conexión establecida con el cliente PID' + str(clientPID))
    if petition['id'] == 1:
        reWrite(fd,toJson(getAllFlights()))
        fd.close()
    if petition['id'] == 2: checkIn(petition['data'],petition['passenger'],petition['seat'])
    if petition['id'] == 3: addFlight(petition['data'])
    if petition['id'] == 4: removeFlight(petition['data'])
    sendSignal(clientPID)
    if petition['id'] == 1: recieveSignal()
    print('Conexión finalizada con el cliente PID' + str(clientPID))