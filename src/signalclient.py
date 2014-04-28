# -'- coding: iso8859-1 -'-

import os
from cfunctions import *
from functions import *
from classes import *
from clientFront import *

####################################################################################################
##### SRV Signal Client v2.0
##### Ejercicio 2.a.1
####################################################################################################

transitionFileName = '.pet.srv'

def getServerPIDandWritePetition(petition):
    fd = open(transitionFileName,'r+')
    global serverPID
    if serverPID == -1:
        serverPID = fd.read()
    fd.seek(0)
    fd.truncate()
    fd.write(petition)
    fd.flush()
    os.fsync(fd.fileno())
    fd.close()
    return int(serverPID)

def signalGetAllFlights():   
    petition = newPetitionMsg(1,str(os.getpid()),None,None,None)
    petition = toJson(petition)
    serverPID = getServerPIDandWritePetition(petition)
    sendSignal(serverPID)
    recieveSignal()
    fd = open(transitionFileName,'r')
    data = fd.read()
    flights = fromJson(data)
    fd.close()
    sendSignal(serverPID)
    return flights

def signalRemoveAFlight(flightID):
    petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
    petition = toJson(petition)
    serverPID = getServerPIDandWritePetition(petition)
    sendSignal(serverPID)
    recieveSignal()

def signalAddAFlight(flight):
    petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
    petition = toJson(petition)
    serverPID = getServerPIDandWritePetition(petition)
    sendSignal(serverPID)
    recieveSignal()
    
def signalCheckIn(flightId, passenger, seat):
    petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
    petition = toJson(petition)
    serverPID = getServerPIDandWritePetition(petition)
    sendSignal(serverPID)
    recieveSignal()

def removeAFlight(flights):
    flightIndex = removeAFlightSelection(flights)
    if flightIndex != -1:
        signalRemoveAFlight(flightIndex)
    
def addAFlight():
    signalAddAFlight(addAFlightInput())

def reserveAFlight(flights):
    selection = reserveASeat(flights)
    if selection != -1:
        signalCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
                   
print('Cliente: Files & Signals')
print("S.R.V. Sistema de Reserva de Vuelos\n")
option = 0;
global serverPID
serverPID = -1
while option != '6':
    mainMenu()
    option = raw_input('Ingrese una Opción: ')
    print('')
    flights = signalGetAllFlights()
    if option == '1': checkAFlight(flights)
    if option == '2': reserveAFlight(flights)
    if option == '3': addAFlight()
    if option == '4': removeAFlight(flights)
    if option == '5': aboutUs()
    if option == '6': quitClient()
