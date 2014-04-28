# -'- coding: iso8859-1 -'-

from clientFront import *
import classes
import cfunctions
import functions
import os

####################################################################################################
##### SRV MQ SV Client v2.0
##### Ejercicio 2.a.4
####################################################################################################

class Client():
    
    def open(self):
        q = cfunctions.mqsvInit();
        self.qin = q['qout']
        self.qout = q['qin']
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toPrettyJson(header)
        cfunctions.mqsvSend(header, self.qout)
        json = 0
        e = True
        json = ''
        while e:
            try:
                s = cfunctions.mqsvReceive(self.qin)
                json = json + s
                response = functions.fromJson(json)
            except ValueError:
                pass
            else:
                e = False
        return functions.toJson(response)

    def MQSVGetAllFlights(self):
        return functions.fromJson(self.request(1))['data']
    
    def reserveAFlight(self,flights):
        selection = reserveASeat(flights)
        if selection != -1:
            self.MQSVCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
    
    def MQSVCheckIn(self,flightId, passenger, seat):
        petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
        petition = functions.toJson(petition)
        cfunctions.mqsvSend(petition, self.qout)
    
    def addAFlight(self):
        self.MQSVAddAFlight(addAFlightInput())
    
    def MQSVAddAFlight(self,flight):
        petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
        petition = functions.toJson(petition)
        cfunctions.mqsvSend(petition, self.qout)
    
    def removeAFlight(self,flights):
        flightIndex = removeAFlightSelection(flights)
        if flightIndex != -1:
            self.MQSVRemoveAFlight(flightIndex)
    
    def MQSVRemoveAFlight(self,flightID):
        petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
        petition = functions.toJson(petition)
        cfunctions.mqsvSend(petition, self.qout)

def main():
    s = Client()   
    s.open()
    print('Cliente: MQ SV')
    print("S.R.V. Sistema de Reserva de Vuelos\n")
    option = 0;
    while option != '6':
        mainMenu()
        option = raw_input('Ingrese una Opción: ')
        print('')
        flights = s.MQSVGetAllFlights()
        if option == '1': checkAFlight(flights)
        if option == '2': s.reserveAFlight(flights)
        if option == '3': s.addAFlight()
        if option == '4': s.removeAFlight(flights)
        if option == '5': aboutUs()
        if option == '6': quitClient()    
        
if __name__ == "__main__":
    main()