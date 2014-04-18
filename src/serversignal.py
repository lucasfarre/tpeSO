from cfunctions import *
from functions import *
from serverback import *
import os

print('Servidor Archivos y Signal')
#'Server crea los archivos de peticiones y respuestas')

petitionfd = open("pet.srv",'w')
petitionfd.close()
#Server espera una signal
#Server recibe una signal

raw_input('Server lee del archivo de peticiones')
#'Server decodifica la peticion
#'Server genera la respuesta y la escribe en el archivo

fd = open("pet.srv",'r+')
petition = fd.read()
petition = fromJson(petition)

fd.seek(0)
fd.truncate()
if petition['id'] == 1:
    #getAllFlights
    data = getAllFlights()
if petition['id'] == 2:
    data = "Prueba de sobreescritura"
fd.write(toJson(data))
fd.flush()
os.fsync(fd.fileno())
fd.close()

#Server envia una signal

