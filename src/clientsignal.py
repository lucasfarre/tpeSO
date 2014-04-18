from cfunctions import *
from functions import *
from classes import *
import os

def clientInit():
    pass

def getServerPID():
    fd = open(".pet.srv",'r+')
    serverPID = fd.read()
    fd.seek(0)
    fd.truncate()
    fd.write(petition)
    fd.flush()
    os.fsync(fd.fileno())
    fd.close()
    return int(serverPID)

print('Cliente: Files & Signals')

#getAllFlights
petition = newPetitionMsg(1,str(os.getpid()))
petition = toJson(petition)
serverPID = getServerPID()
sendSignal(serverPID)
recieveSignal()
fd = open(".pet.srv",'r')
print fd.read()
fd.close()
sendSignal(serverPID)