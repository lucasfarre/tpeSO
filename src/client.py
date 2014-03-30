from clientback import flightStatus, checkIn
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

checkIn(0, newPassenger(36000000, "Jorge Gutierrez", "ARG", "03/08/1992"), Seat(3, "A", None, None))
