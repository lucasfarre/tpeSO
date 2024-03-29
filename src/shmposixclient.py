# -'- coding: iso8859-1 -'-

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
    
    def open(self):
        self.mem = cfunctions.getmemPosix()
        self.sd1 = cfunctions.initmutexPosix('/sem1', -1)
        self.sd2 = cfunctions.initmutexPosix('/sem2', -1)
        self.sd3 = cfunctions.initmutexPosix('/sem3', -1)
    
    def request(self, id):
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toPrettyJson(header)
        cfunctions.semwait(self.sd1)
        cfunctions.memwrite(self.mem, header)
        cfunctions.sempost(self.sd2)
        cfunctions.semwait(self.sd3)
        json = cfunctions.memread(self.mem)
        cfunctions.sempost(self.sd1)
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
        cfunctions.semwait(self.sd1)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.sempost(self.sd2)
        cfunctions.semwait(self.sd3)
        cfunctions.sempost(self.sd1)
        
    def addAFlight(self):
        self.SHMPosixAddAFlight(addAFlightInput())
    
    def SHMPosixAddAFlight(self,flight):
        petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
        petition = functions.toJson(petition)
        cfunctions.semwait(self.sd1)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.sempost(self.sd2)
        cfunctions.semwait(self.sd3)
        cfunctions.sempost(self.sd1)
    
    def removeAFlight(self,flights):
        flightIndex = removeAFlightSelection(flights)
        if flightIndex != -1:
            self.SHMPosixRemoveAFlight(flightIndex)
    
    def SHMPosixRemoveAFlight(self,flightID):
        petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
        petition = functions.toJson(petition)
        cfunctions.semwait(self.sd1)
        cfunctions.memwrite(self.mem, petition)
        cfunctions.sempost(self.sd2)
        cfunctions.semwait(self.sd3)
        cfunctions.sempost(self.sd1)
            
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
