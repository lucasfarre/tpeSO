from dbback import *
import classes
import cfunctions
import socket
import functions

####################################################################################################
##### SRV SHM System V Client v2.0
##### Ejercicio 2.a.2
####################################################################################################

class Server:

    def open(self):
        self.mem = cfunctions.getmem()
        cfunctions.memset(self.mem, 0, 10000)
        self.semid = -1
        while self.semid == -1:
			self.semid = cfunctions.initmutex()
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            while self.semid == -1:
				self.semid = cfunctions.initmutex()
            cfunctions.down(self.semid, 2)
            json = cfunctions.memread(self.mem)
            print 'Peticion Recibida: \n' + functions.toPrettyJson(functions.fromJson(json))
            request = functions.fromJson(json)
            id = int(request['id'])
            if id == 1:
                response = classes.package('0001', '0000000', getAllFlights())
                response = functions.toJson(response)
                cfunctions.memwrite(self.mem, response)
                cfunctions.up(self.semid, 3)
            if id == 2:
                checkIn(request['data'],request['passenger'],request['seat'])
                cfunctions.up(self.semid, 3)
            if id == 3:
                addFlight(request['data'])
                cfunctions.up(self.semid, 3)
            if id == 4: 
                removeFlight(request['data'])
                cfunctions.up(self.semid, 3)
            if id == 6:
				cfunctions.up(self.semid, 3)
				cfunctions.removeSem(self.semid)
				self.semid = -1
                
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main() 
