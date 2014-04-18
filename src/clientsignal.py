from cfunctions import *
from functions import *
from classes import *
import os

print('Cliente Archivos y Signal')
#Cliente sabe la ubicacion del archivo de intercambio
#Al final no use la createFile y closeFile de cfunctions

raw_input('Cliente escribe en un archivo la instruccion')
petition = newPetitionMsg(1,'Prueba')
petition = toJson(petition)
fd = open("pet.srv",'r+')
fd.seek(0)
fd.truncate()
fd.write(petition)
fd.flush()
os.fsync(fd.fileno())
fd.close()

#Cliente envia una signal al server
#Cliente recibe signal del server

raw_input('Cliente lee en un archivo la respuesta')
fd = open("pet.srv",'r')
print fd.read()
fd.close()