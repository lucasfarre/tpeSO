from cfunctions import *
from functions import *
from classes import *
import os

print('Cliente Archivos y Signal')
#Cliente sabe la ubicacion del archivo de intercambio
#Al final no use la createFile y closeFile de cfunctions
#print os.getpid()
print('Client PID ' + str(os.getpid()))
#print('Cliente escribe en un archivo la instruccion')
petition = newPetitionMsg(1,str(os.getpid()))
petition = toJson(petition)
#print petition
fd = open(".pet.srv",'r+')
serverpid = fd.read()
fd.seek(0)
fd.truncate()
fd.write(petition)
fd.flush()
os.fsync(fd.fileno())
fd.close()

#Cliente envia una signal al server

#serverpid = raw_input('PID: ')
print('Server PID:' + serverpid)
sendSignal(int(serverpid))

#Cliente recibe signal del server

recieveSignal()

#print('Cliente lee en un archivo la respuesta')
fd = open(".pet.srv",'r')
print fd.read()
fd.close()

sendSignal(int(serverpid))
