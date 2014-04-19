from cfunctions import *
from functions import *
from serverback import *
import os

def serverInit():
    petitionfd = open(".pet.srv",'w')
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
    recieveSignal()
    fd = open(".pet.srv",'r+')
    petition = fd.read()
    petition = fromJson(petition)
    clientPID = getClientPID(petition)
    fd.seek(0)
    fd.truncate()
    if petition['id'] == 1:
        #getAllFlights
        data = getAllFlights()
        fd.write(toJson(data))
        fd.flush()
        os.fsync(fd.fileno())
        fd.close()
        sendSignal(clientPID)
        recieveSignal()
    if petition['id'] == 2:
        #checkIn
        checkIn(petition['data'],petition['passenger'],petition['seat'])
        fd.flush()
        os.fsync(fd.fileno())
        fd.close()
        sendSignal(clientPID)
    if petition['id'] == 3:
        #addAFlight
        addFlight(petition['data'])
        fd.flush()
        os.fsync(fd.fileno())
        fd.close()
        sendSignal(clientPID)
    if petition['id'] == 4:
        #removeAFlight
        removeFlight(petition['data'])
        fd.flush()
        os.fsync(fd.fileno())
        fd.close()
        sendSignal(clientPID)