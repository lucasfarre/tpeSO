# -'- coding: iso8859-1 -'-

import classes
import cfunctions
import functions
import time
import os
from clientFront import *

####################################################################################################
##### SRV SHM System V Client v2.0
##### Ejercicio 2.a.2
####################################################################################################

class Client():
    
    def open(self):
        self.mem = cfunctions.getmem()
        self.semid = -1
        while self.semid == -1:
			self.semid = cfunctions.initmutex()

    def request(self, id):
        header = classes.package(str(id).zfill(4), '0000060', time.time())
        header = functions.toJson(header)
        cfunctions.down(self.semid, 1)
        cfunctions.memwrite(self.mem, header)
        cfunctions.up(self.semid, 2)        
        cfunctions.down(self.semid, 3)
        json = cfunctions.memread(self.mem)
        cfunctions.up(self.semid, 1)
        return json

    def SHMSVGetAllFlights(self):
        aux = self.request(1)
        return functions.fromJson(aux)['data']

    def reserveAFlight(self,flights):
        selection = reserveASeat(flights)
        if selection != -1:
            self.SHMSVCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
    
    def SHMSVCheckIn(self,flightId, passenger, seat):
        petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
        petition = functions.toJson(petition)
        cfunctions.down(self.semid, 1)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.up(self.semid, 2)        
        cfunctions.down(self.semid, 3)
        cfunctions.up(self.semid, 1)   
        
    def addAFlight(self):
        self.SHMSVAddAFlight(addAFlightInput())
    
    def SHMSVAddAFlight(self,flight):
        petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
        petition = functions.toJson(petition)
        cfunctions.down(self.semid, 1)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.up(self.semid, 2)        
        cfunctions.down(self.semid, 3)
        cfunctions.up(self.semid, 1)         
    
    def removeAFlight(self,flights):
        flightIndex = removeAFlightSelection(flights)
        if flightIndex != -1:
            self.SHMSVRemoveAFlight(flightIndex)
    
    def SHMSVRemoveAFlight(self,flightID):
        petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
        petition = functions.toJson(petition)
        cfunctions.down(self.semid, 1)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.up(self.semid, 2)        
        cfunctions.down(self.semid, 3)
        cfunctions.up(self.semid, 1)  
    
    def SHMSVquitClient(self):
        self.request(6)
        
        
def main():
    s = Client()
    print('Cliente: SHM Posix')
    print("S.R.V. Sistema de Reserva de Vuelos\n")
    option = 0;
    while option != '6':
        s.open()
        mainMenu()
        option = raw_input('Ingrese una Opción: ')
        print('')
        flights = s.SHMSVGetAllFlights()
        if option == '1': checkAFlight(flights)
        if option == '2': s.reserveAFlight(flights)
        if option == '3': s.addAFlight()
        if option == '4': s.removeAFlight(flights)
        if option == '5': aboutUs()
        if option == '6': s.SHMSVquitClient()
        
if __name__ == "__main__":
    main()
