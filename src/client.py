# -'- coding: iso8859-1 -'-

from clientback import *
from flight import *
from classes import *
import sys
import os


print("S.R.V. Sistema de Reserva de Vuelos")

# user = raw_input("user: ")
# password = raw_input("password: ")
# print("")
# print("1. Reservar Vuelo")
# print("2. Consultar Vuelo")
# print("3. Agregar Vuelo")
# print("3. Modificar Vuelo")
# print("4. Eliminar Vuelo")
# print("5. Salir")
# print("")
# 
# option = raw_input("Ingrese una opcion: ")

option = '1'
 
if option == "1":
    print('Vuelos disponibles:\n')
    print('#     Vuelo    Salida           Llegada')
    print('-----------------------------------------------')
    i = 1
    flights = getAllFlights()
    for f in flights:
        print(str(i) + '     ' + str(f['id']) + '   ' + f['departDate'] + ' ' + f['departAirport'] + '   ' + f['arriveDate'] + ' ' + f['arriveAirport'])
        i = i + 1
    print('')
    j = raw_input("Seleccione un vuelo: ")
    while int(j) <= 0 or int(j) >= i:
        j = raw_input("Seleccione un vuelo: ")
    #print flights[int(j) - 1]
    
    id = raw_input('Ingrese su número pasaporte: ')
    name = raw_input('Ingrese su nombre completo: ')
    nationality = raw_input('Ingrese su nacionalidad: ')
    birthday = raw_input('Ingrese su fecha de nacimiento: ')
    
    print('Asientos disponibles: \n')
    flight = flights[int(j) - 1]
    for column in list(flight['aircraft']['seatsColumns']):
        print('     ' + column + '   '),
    print('')
    print('--------------------------------------------------------------')
    for i in range(1, flight['aircraft']['seatsRows'] + 1):
        sys.stdout.write(str(i) + '   ')
        if i < 10:
            sys.stdout.write(' ')
        for j in list(flight['aircraft']['seatsColumns']):
            for seat in flight['aircraft']['seats']:
                if seat['row'] == i and seat['column'] == j:
                    if seat['status']:
                        sys.stdout.write('Ocupado   ')
                    else:
                        sys.stdout.write('Libre     ')
        print('')
    print('')
    
    row = raw_input("Seleccione fila: ")
    column = raw_input("Seleccione columna: ")    
    if int(row) >= 1 and int(row) <= flight['aircraft']['seatsRows']:
        if column in flight['aircraft']['seatsColumns']:
            for seat in flight['aircraft']['seats']:
                if seat['row'] == int(row) and seat['column'] == column:
                    if seat['status'] == False:
                        checkIn(flight['id'], newPassenger(id, name, nationality, birthday), seat)
                    else:
                        print("Asiento Ocupado")
                    

# addFlight(newFlight("AA3456","30/03/2014","EZE","31/03/2014","LAX",True,None))
# addFlight(newFlight("LN2345","12/04/2014","JNW","12/04/2014","MDZ",True,None))
# removeFlight("AA3456")
# modifyFlight(newFlight("LN2345","11/05/2014","JNW","11/05/2014","MDZ",True,None))
# print flightStatus("LN2345")
# checkIn(0, newPassenger(30657483, "Jorge Lorenzon", "CHI", "05/12/1989"), Seat(29, "F", None, None))