from dbback import *
import classes
import cfunctions
import socket
import functions

####################################################################################################
##### SRV SHM Posix Server v2.0
##### Ejercicio 2.a.2
####################################################################################################

class Server:

    def open(self):
        self.mem = cfunctions.getmemPosix()
        self.sd = cfunctions.initmutexPosix()
        print str(self.mem)
        print str(self.sd)
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            cfunctions.semwait(self.sd)
            json = cfunctions.memread(self.mem)
            print 'Request received: \n' + json
            request = functions.fromJson(json)
            id = int(request['id'])
            if id == 1:
                response = classes.package('0001', '0000000', getAllFlights())
                response = functions.toJson(response)
                cfunctions.sempost(self.sd)
                cfunctions.memwrite(self.mem, response)
                cfunctions.semwait(self.sd)
            if id == 2: 
                checkIn(request['data'],request['passenger'],request['seat'])
            if id == 3:
                addFlight(request['data'])
            if id == 4: 
                removeFlight(request['data'])
        
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()