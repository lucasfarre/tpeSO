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
        print 'Dir de memoria: ' + str(self.mem)
        self.sd1 = cfunctions.initmutexPosix('/sem1', 1)
        self.sd2 = cfunctions.initmutexPosix('/sem2', 0)
        self.sd3 = cfunctions.initmutexPosix('/sem3', 0)
        
    def run(self):
        self.open()
        up = 1
        while up == 1:
            cfunctions.semwait(self.sd2)
            json = cfunctions.memread(self.mem)
            print 'Request received: \n' + json
            request = functions.fromJson(json)
            id = int(request['id'])
            if id == 1:
                response = classes.package('0001', '0000000', getAllFlights())
                response = functions.toJson(response)
                cfunctions.memwrite(self.mem, response)
                cfunctions.sempost(self.sd3)
            if id == 2: 
                checkIn(request['data'],request['passenger'],request['seat'])
                cfunctions.sempost(self.sd3)
            if id == 3:
                addFlight(request['data'])
                cfunctions.sempost(self.sd3)
            if id == 4: 
                removeFlight(request['data'])
                cfunctions.sempost(self.sd3)
        
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()
