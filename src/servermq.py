from classes import *
from functions import fromJson, toJson
from serverback import *
from cfunctions import *

print('Servidor de la Cola de Mensajes')

q = cfunctions.msgServerInit();
print('qin = '+ str(q['qin']))
print('qout = '+ str(q['qout']))

while True:
    input = cfunctions.msgServerRecieve(q['qin'])
    if input['id'] == 4:
        print input
#    if input['id'] != -1:
#	    petition = fromJson(input['mtext'])
#    if petition['id'] == 1:
#        print('Se solicito la opcion 1')
#        flights = getAllFlights()
#        petition['data'] = flights
#        msg = toJson(petiton)
#        print('Respondiendo la solicitud')
#        cfunctions.sendMessage(msg)