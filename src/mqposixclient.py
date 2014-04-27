# -'- coding: iso8859-1 -'-

import classes
import cfunctions
import functions
import os
from clientFront import *

####################################################################################################
##### SRV MQ Posix Client v2.0
##### Ejercicio 2.a.4
####################################################################################################

class Client():
    
    def open(self):
        self.qin = '/qout'
        self.qout = '/qin'
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toPrettyJson(header)
        cfunctions.mqposixSend(header, self.qout)
        json = 0
        e = True
        json = ''
        while e:
            try:
                s = cfunctions.mqposixReceive(self.qin)
                json = json + s
                response = functions.fromJson(json)
            except ValueError:
                pass
            else:
                e = False
        return functions.toJson(response)
    
    def MQPosixGetAllFlights(self):
        return functions.fromJson(self.request(1))['data']
    
    def reserveAFlight(self,flights):
        selection = reserveASeat(flights)
        if selection != -1:
            self.MPPosixCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
    
    def MPPosixCheckIn(self,flightId, passenger, seat):
        petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
        petition = functions.toJson(petition)
        cfunctions.mqposixSend(petition, self.qout)
    
def main():
    s = Client()   
    s.open()
    print('Cliente: MQ Posix')
    print("S.R.V. Sistema de Reserva de Vuelos\n")
    option = 0;
    while option != '6':
        mainMenu()
        option = raw_input('Ingrese una Opción: ')
        print('')
        flights = s.MQPosixGetAllFlights()
        if option == '1': checkAFlight(flights)
        if option == '2': s.reserveAFlight(flights)
        if option == '3': s.addAFlight()
        if option == '4': s.removeAFlight(flights)
        if option == '5': aboutUs()
        if option == '6': quitClient()    
        
if __name__ == "__main__":
    main()
