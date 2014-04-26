# -'- coding: iso8859-1 -'-

import dbback
import classes
import cfunctions
import socket
import functions
import os
from clientFront import *

####################################################################################################
##### SRV Socket Client v2.0
##### Ejercicio 2.b
####################################################################################################

class Client:
    
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
    
    def open(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.clientfd = cfunctions.clientInit(self.__ip, int(self.__port))
    
    def close(self):
        cfunctions.clientDown(self.clientfd)
    
    def request(self, id):
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toJson(header)
        cfunctions.writen(self.clientfd, header, 60)
        json = cfunctions.readn(self.clientfd, 60)[1]
        if len(json) >= 60:
            json = json[:60]
            header = functions.fromJson(json)
            length = int(header['length'])
            json = cfunctions.readn(self.clientfd, length)[1]
            if len(json) >= length:
                json = json[:length]
                response = functions.fromJson(json)
                return response
        #Ojo
        #self.close()    
        
    def SocketGetAllFlights(self):   
        return self.request(1)['data']
    
    def reserveAFlight(self,flights):
        selection = reserveASeat(flights)
        if selection != -1:
            self.SocketCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
    
    def SocketCheckIn(self,flightId, passenger, seat):
        petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
        petition = functions.toJson(petition)
        print petition
        header = classes.package('0002', str(len(petition)).zfill(7), None)
        header = functions.toJson(header)
        cfunctions.writen(self.clientfd, header, 60) 
        cfunctions.writen(self.clientfd, petition, len(petition))  
        
    def addAFlight(self):
        flight = addAFlightInput()
        self.SocketAddAFlight(flight)

    def SocketAddAFlight(self,flight):
        petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
        petition = functions.toJson(petition)
        print petition
        header = classes.package('0003', str(len(petition)).zfill(7), None)
        header = functions.toJson(header)
        cfunctions.writen(self.clientfd, header, 60) 
        cfunctions.writen(self.clientfd, petition, len(petition)) 

    def removeAFlight(self,flights):
        flightIndex = removeAFlightSelection(flights)
        if flightIndex != -1:
            self.SocketRemoveAFlight(flightIndex)
    
    def SocketRemoveAFlight(self,flightID):
        petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
        petition = functions.toJson(petition)
        print petition
        header = classes.package('0004', str(len(petition)).zfill(7), None)
        header = functions.toJson(header)
        cfunctions.writen(self.clientfd, header, 60) 
        cfunctions.writen(self.clientfd, petition, len(petition)) 
        
    def SocketQuitClient(self):
        #header = classes.package('0006','0'.zfill(7), None)
        #header = functions.toJson(header)
        #cfunctions.writen(self.clientfd, header, 60) 
        self.close()    
        
def main():
    ip = raw_input('Ingrese el IP del servidor: ')
    port = raw_input('Ingrese el puerto del servidor: ')
    s = Client(ip, port)
    s.open()
    print('Cliente: Socket')
    print("S.R.V. Sistema de Reserva de Vuelos\n")
    option = 0;
    while option != '6':
        mainMenu()
        option = raw_input('Ingrese una Opción: ')
        print('')
        flights = s.SocketGetAllFlights()
        if option == '1': checkAFlight(flights)
        if option == '2': s.reserveAFlight(flights)
        if option == '3': s.addAFlight()
        if option == '4': s.removeAFlight(flights)
        if option == '5': aboutUs()
        if option == '6': s.SocketQuitClient()
        
if __name__ == "__main__":
    main()
