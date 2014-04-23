# -'- coding: iso8859-1 -'-

import dbback
import classes
import cfunctions
import functions
import os
from clientFront import *

####################################################################################################
##### SRV SHM Posix Client v2.0
##### Ejercicio 2.a.2
####################################################################################################

class Client():
    
    def __init__(self):
        pass
    
    def open(self):
        self.mem = cfunctions.getmemPosix()
        self.sd = cfunctions.initmutexPosix()
        print str(self.mem)
        print str(self.sd)
    
    def request(self, id):
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toJson(header)
        cfunctions.memwrite(self.mem, header)
        cfunctions.sempost(self.sd)
        cfunctions.semwait(self.sd)
        json = cfunctions.memread(self.mem)
        cfunctions.sempost(self.sd)
        return json

    def SHMPosixGetAllFlights(self):
        return functions.fromJson(self.request(1))['data']

    def reserveAFlight(self,flights):
        selection = reserveASeat(flights)
        if selection != -1:
            self.SHMPosixCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
    
    def SHMPosixCheckIn(self,flightId, passenger, seat):
        petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
        petition = functions.toJson(petition)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.sempost(self.sd)
        
    def addAFlight(self):
        self.SHMPosixAddAFlight(addAFlightInput())
    
    def SHMPosixAddAFlight(self,flight):
        petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
        petition = functions.toJson(petition)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.sempost(self.sd)
    
    def removeAFlight(self,flights):
        flightIndex = removeAFlightSelection(flights)
        if flightIndex != -1:
            self.SHMPosixRemoveAFlight(flightIndex)
    
    def SHMPosixRemoveAFlight(self,flightID):
        petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
        petition = functions.toJson(petition)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.sempost(self.sd)
            
def main():
    s = Client()
    s.open()
    print('Cliente: SHM Posix')
    print("S.R.V. Sistema de Reserva de Vuelos\n")
    option = 0;
    while option != '6':
        mainMenu()
        option = raw_input('Ingrese una Opci�n: ')
        print('')
        flights = s.SHMPosixGetAllFlights()
        if option == '1': checkAFlight(flights)
        if option == '2': s.reserveAFlight(flights)
        if option == '3': s.addAFlight()
        if option == '4': s.removeAFlight(flights)
        if option == '5': aboutUs()
        if option == '6': quitClient()
        
if __name__ == "__main__":
    main()        