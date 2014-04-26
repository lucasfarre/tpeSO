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
        #TODO MAX_LONG?
        self.semid = cfunctions.initmutex()
        print str(self.mem)
        print str(self.semid)
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            cfunctions.down(self.semid, 2)
            json = cfunctions.memread(self.mem)
            print 'Request received: \n' + json
            request = functions.fromJson(json)
            id = int(request['id'])
            if id == 1:
                response = classes.package('0001', '0000000', getAllFlights())
                response = functions.toJson(response)
                cfunctions.memwrite(self.mem, response)
                cfunctions.up(self.semid, 3)
            if id == 2:
                checkIn(request['data'],request['passenger'],request['seat'])
            if id == 3:
                addFlight(request['data'])
            if id == 4: 
                removeFlight(request['data'])
            if id == 6:
                cfunctions.up(self.semid, 3)
                cfunctions.memset(self.mem, 0, 10000)
                self.semid = cfunctions.initmutex()
                #up = 0
                
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main() 