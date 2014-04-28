# -'- coding: iso8859-1 -'-

import os
import cfunctions
import functions
import classes
from clientFront import *

####################################################################################################
##### SRV Fifo Client v2.0
##### Ejercicio 2.a.3
####################################################################################################

class FifoClient:
        
    def close(self):
		cfunctions.unlock(self.clientfdrequest)
		os.close(self.clientfdresponse)
		os.close(self.clientfdrequest)
    
    def connect(self):
        self.clientfdresponse = os.open('/tmp/fiforesponse', os.O_RDONLY)
        error = True
        while error:
			try: 
				self.clientfdrequest = os.open('/tmp/fiforequest', os.O_WRONLY)
			except OSError:
				pass
			else:
				error = False
				print 'Por favor espere...'
				cfunctions.lock(self.clientfdrequest)
    
    def open(self, mode):
        if mode == os.O_RDONLY:
            self.clientfdresponse = os.open('/tmp/fiforesponse', mode)
        else:
            self.clientfdrequest = os.open('/tmp/fiforequest', mode)
    
    def request(self, id):
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toPrettyJson(header)
        cfunctions.writen(self.clientfdrequest, header, 60)
        json = cfunctions.readn(self.clientfdresponse, 60)[1]
        if len(json) >= 60:
            json = json[:60]
            header = functions.fromJson(json)
            length = int(header['length'])
            json = cfunctions.readn(self.clientfdresponse, length)[1]
            if len(json) >= length:
                json = json[:length]
                response = functions.fromJson(json)
                return response
        
            
    def FifoGetAllFlights(self):   
        return self.request(1)['data']
    
    def reserveAFlight(self,flights):
        selection = reserveASeat(flights)
        if selection != -1:
            self.FifoCheckIn(selection['flightId'], selection['passenger'], selection['seat'])
    
    def FifoCheckIn(self,flightId, passenger, seat):
        petition = newPetitionMsg(2,str(os.getpid()),flightId,passenger,seat)
        petition = functions.toJson(petition)
        print petition
        header = classes.package('0002', str(len(petition)).zfill(7), None)
        header = functions.toPrettyJson(header)
        cfunctions.writen(self.clientfdrequest, header, 60) 
        cfunctions.writen(self.clientfdrequest, petition, len(petition))  
        
    def addAFlight(self):
        flight = addAFlightInput()
        self.FifoAddAFlight(flight)

    def FifoAddAFlight(self,flight):
        petition = newPetitionMsg(3,str(os.getpid()),flight,None,None)
        petition = functions.toJson(petition)
        print petition
        header = classes.package('0003', str(len(petition)).zfill(7), None)
        header = functions.toPrettyJson(header)
        cfunctions.writen(self.clientfdrequest, header, 60) 
        cfunctions.writen(self.clientfdrequest, petition, len(petition)) 

    def removeAFlight(self,flights):
        flightIndex = removeAFlightSelection(flights)
        if flightIndex != -1:
            self.FifoRemoveAFlight(flightIndex)
    
    def FifoRemoveAFlight(self,flightID):
        petition = newPetitionMsg(4,str(os.getpid()),flightID,None,None)
        petition = functions.toJson(petition)
        print petition
        header = classes.package('0004', str(len(petition)).zfill(7), None)
        header = functions.toPrettyJson(header)
        cfunctions.writen(self.clientfdrequest, header, 60) 
        cfunctions.writen(self.clientfdrequest, petition, len(petition)) 

def main():
    s = FifoClient()
    print('Cliente: Fifo')
    print("S.R.V. Sistema de Reserva de Vuelos\n")
    option = 0;
    while option != '6':
		s.connect()
		mainMenu()
		option = raw_input('Ingrese una Opción: ')
		print('')
		flights = s.FifoGetAllFlights()
		if option == '1': checkAFlight(flights)
		if option == '2': s.reserveAFlight(flights)
		if option == '3': s.addAFlight()
		if option == '4': s.removeAFlight(flights)
		if option == '5': aboutUs()
		if option == '6': quitClient()
		s.close()
            
if __name__ == "__main__":
    main()
