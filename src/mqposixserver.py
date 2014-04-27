from dbback import *
import classes
import cfunctions
import functions
import os
import string

####################################################################################################
##### SRV MQ Posix Server v2.0
##### Ejercicio 2.a.4
####################################################################################################

class Server:

    def open(self):
        self.qin = '/qin'
        self.qout = '/qout'
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            open = True
            json = 0
            while not isinstance(json, str):
                json = cfunctions.mqposixReceive(self.qin)
            print 'Peticion Recibida: \n' + json
            request = functions.fromJson(json)
            id = int(request['id'])
            if id == 1:
                response = classes.package('0001', '0000000', getAllFlights())
                response = functions.toPrettyJson(response)
                l = string.split(response)
                for s in l:
                    print s
                    errno = cfunctions.mqposixSend(s, self.qout)
                    if errno != 0:
                        os.strerror(errno)       
                print 'mande'
            if id == 2:
                checkIn(request['data'],request['passenger'],request['seat'])

        
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()  
