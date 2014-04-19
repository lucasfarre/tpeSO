# -'- coding: iso8859-1 -'-

from classes import *
import sys

####################################################################################################
##### SRV Front Client v2.0 
##### Com�n para todas las implementaciones
####################################################################################################

def printAllFlights(flights):
    print('Vuelos disponibles:\n')
    print('#     Vuelo    Salida           Llegada')
    print('-----------------------------------------------')
    i = 1
    for f in flights:
        print(str(i) + '     ' + str(f['id']) + '   ' + f['departDate'] + ' ' + f['departAirport'] + '   ' + f['arriveDate'] + ' ' + f['arriveAirport'])
        i = i + 1
    print('\n')
    
def printFlightStatus(flightIndex, flights):
    flight = flights[int(flightIndex) - 1]
    print('##############################################')
    print('Asientos Disponibles del Vuelo ' + flight['id'])
    print('Salida: ' + flight['departDate'] + ' ' + flight['departAirport'] )
    print('Llegada: ' + flight['arriveDate'] + ' ' + flight['arriveAirport'] )
    print('##############################################')
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

def checkAFlight(flights):    
    i = len(flights)
    if i == 0:
        print('No hay ning�n vuelo en la base de datos')
    else:
        printAllFlights(flights)
        j = raw_input("Indique el N�mero de Vuelo: ")
        while int(j) <= 0 or int(j) > i :
            j = raw_input("N�mero de Vuelo Incorrecto\nIndique el N�mero de Vuelo: ")
        printFlightStatus(j,flights)  
    
def mainMenu():
    print('Men� de Opciones')
    print('##################################')
    print('1. Consultar el estado de un Vuelo')
    print('2. Reservar un Vuelo')
    print('3. Agregar un Vuelo')
    print('4. Quitar un Vuelo')
    print('5. Acerca De')
    print('6. Salir')
    print('')
    
def aboutUs():
    print('SRV es un sistema desarrollado en Python y C\npor Lucas Farr� y Franco Meola\npara la materia Sistemas Operativos\n')
    
def quitClient():
    print('Gracias por utilizar el Sistema de Reserva de Vuelos.')
    
def addAFlightInput():
    print('Agregar un Vuelo')
    print('####################')
    #Armado del Aircraft
    id = raw_input('Ingrese el ID del Avi�n: ')
    model = raw_input('Ingrese el modelo del Avi�n: ')
    print('El avi�n contar� con seis columnas de asientos')
    row = raw_input('Ingrese el N�mero de Filas de Asientos: ')
    defaultColumns = list('ABCDEF')
    seats = []
    for i in range(1, int(row)+1):
        for j in defaultColumns:
            seats.append(newSeat(i, j, False, False))
    aircraft = newAircraft(id, model, seats, i, defaultColumns)
    #Armado del Vuelo
    id = raw_input('Ingrese el ID del Vuelo: ')
    departDate = raw_input('Ingrese la fecha de salida del Vuelo: ')
    departAirport = raw_input('Ingrese el c�digo del Aeropuerto de Salida: ')
    arriveDate = raw_input('Ingrese la fecha de llegada del Vuelo: ')
    arriveAirport = raw_input('Ingrese el c�digo del Aeropuerto de Llegada: ')
    flight = newFlight(id, departDate, departAirport, arriveDate, arriveAirport, True, aircraft)
    return flight

def removeAFlightSelection(flights):
    print('Eliminar un Vuelo')
    print('####################')
    i = len(flights)
    if i == 0:
        print('No hay ning�n vuelo en la base de datos')
        return -1
    else:
        printAllFlights(flights)
        j = raw_input("Indique el N�mero de Vuelo a eliminar:")
        while int(j) <= 0 or int(j) > i :
            j = raw_input("N�mero de Vuelo Incorrecto\nIndique el N�mero de Vuelo a eliminar:")
        return int(j)-1
    
def reserveASeat(flights):
    print('Reservar un Asiento')
    print('####################')
    i = len(flights)
    if i == 0:
        print('No hay ning�n vuelo en la base de datos')
        return -1
    else:
        printAllFlights(flights)
        j = raw_input("Indique el N�mero de Vuelo: ")
        while int(j) <= 0 or int(j) > i:
            j = raw_input("Indique el N�mero de Vuelo: ")
        id = raw_input('Ingrese su n�mero pasaporte: ')
        name = raw_input('Ingrese su nombre completo: ')
        nationality = raw_input('Ingrese su nacionalidad: ')
        birthday = raw_input('Ingrese su fecha de nacimiento: ')
        passenger = newPassenger(id, name, nationality, birthday)
        flight = flights[int(j) - 1]
        print('##############################################')
        print('Seleccion del Asiento para el Vuelo ' + flight['id'])
        print('Salida: ' + flight['departDate'] + ' ' + flight['departAirport'] )
        print('Llegada: ' + flight['arriveDate'] + ' ' + flight['arriveAirport'] )
        print('##############################################')
        print('')
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
        print('##############################################')
        #TODO: Agregar si elige mal el asiento, no hacer todo de nuevo
        row = raw_input("Indique la Fila del Asiento: ")
        #TODO: Validar si ingres� una letra o un n�mero
        column = raw_input("Indique la Columna del Asiento: ")
        column = column.upper() 
        if int(row) >= 1 and int(row) <= flight['aircraft']['seatsRows']:
            if column in flight['aircraft']['seatsColumns']:
                for seat in flight['aircraft']['seats']:
                    if seat['row'] == int(row) and seat['column'] == column:
                        if seat['status'] == False:
                            return {'flightId': flight['id'], 'passenger': passenger, 'seat': seat }
                        else:
                            print("Asiento Ocupado\n")
                            return -1