from classes import *
from cfunctions import *
from functions import fromJson, toJson

print('Cliente de la Cola de Mensajes')

q = msgServerInit();
print('qin = '+ str(q['qin']))
print('qout = '+ str(q['qout']))

while True:
    raw_input('Solicito al servidor la opcion 1')
    petition = newPetitionMsg(1,'Prueba')
    petition = toJson(petition)
    print('Enviando mensaje al servidor')
    response = msgClientSendAndReceive(petition,q['qin'],q['qout'])
    print('Respuesta recibida')
    print response
