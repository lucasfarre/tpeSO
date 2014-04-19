# -'- coding: iso8859-1 -'-

from clientFront import *
from dbback import *
import sys
import os

####################################################################################################
##### SRV Local Client v2 
####################################################################################################

def addAFlight():
    addFlight(addAFlightInput())
               
def removeAFlight(flights):
    flightIndex = removeAFlightSelection(flights)
    if flightIndex != -1:
        removeFlight(flightIndex)

def reserveAFlight(flights):
    selection = reserveASeat(flights)
    if selection != -1:
        checkIn(selection['flightId'], selection['passenger'], selection['seat'])

####################################################################################################
##### Main
####################################################################################################

print("S.R.V. Sistema de Reserva de Vuelos\n")
option = 0;
while option != '6':
    mainMenu()
    option = raw_input('Ingrese una Opci�n: ')
    print('')
    flights = getAllFlights()
    if option == '1': checkAFlight(flights)
    if option == '2': reserveAFlight(flights)
    if option == '3': addAFlight()
    if option == '4': removeAFlight(flights)
    if option == '5': aboutUs()
    if option == '6': quitClient()