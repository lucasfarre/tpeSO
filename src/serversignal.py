from cfunctions import *
from functions import *
from serverback import *
import os

print('Servidor Archivos y Signal')
#'Server crea los archivos de peticiones y respuestas')
#print os.getpid()
#petitionfd = open("pet.srv",'w')
#petitionfd.close()
#Server espera una signal

while True:
    petitionfd = open(".pet.srv",'w')
    petitionfd.seek(0)
    petitionfd.truncate()
    petitionfd.write(str(os.getpid()))
    print('Server PID: ' + str(os.getpid()))
    petitionfd.flush()
    os.fsync(petitionfd.fileno())
    petitionfd.close()
    aux = recieveSignal()
    #Server recibe una signal
    
    #print('Server lee del archivo de peticiones')
    #'Server decodifica la peticion
    #'Server genera la respuesta y la escribe en el archivo
    
    fd = open(".pet.srv",'r+')
    petition = fd.read()
    petition = fromJson(petition)
    #print petition
    clientpid = petition['data']
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
    
    #clientpid = raw_input('PID: ')
    print('Client PID ' + clientpid)
    sendSignal(int(clientpid))

    aux = recieveSignal()

