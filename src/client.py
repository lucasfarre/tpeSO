# -'- coding: iso8859-1 -'-

from clientback import *
from flight import *
from classes import *

print("S.R.V. Sistema de Reserva de Vuelos")

# user = raw_input("user: ")
# password = raw_input("password: ")
print("")
print("1. Reservar Vuelo")
print("2. Consultar Vuelo")
print("3. Agregar Vuelo")
print("3. Modificar Vuelo")
print("4. Eliminar Vuelo")
print("5. Salir")
print("")
# option = raw_input("Ingrese una opcion: ")
 
# if option == "1":
# flight = raw_input("Ingrese el numero de vuelo: ")
# flightStatus(flight)
# 
# flightStatus(1)

addFlight(newFlight("AA3456","30/03/2014","EZE","31/03/2014","LAX",True,None))
addFlight(newFlight("LN2345","12/04/2014","JNW","12/04/2014","MDZ",True,None))
removeFlight("AA3456")
modifyFlight(newFlight("LN2345","11/05/2014","JNW","11/05/2014","MDZ",True,None))
print flightStatus("LN2345")
checkIn(0, newPassenger(30657483, "Jorge Lorenzon", "CHI", "05/12/1989"), Seat(29, "F", None, None))