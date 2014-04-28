from dbback import *
import classes
import cfunctions
import functions
import os
import string

####################################################################################################
##### SRV MQ SV Server v2.0
##### Ejercicio 2.a.4
####################################################################################################

class Server():

    def open(self):
        q = cfunctions.mqsvInit();
        self.qin = q['qin']
        self.qout = q['qout']
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            open = True
            json = 0
            while not isinstance(json, str):
                json = cfunctions.mqsvReceive(self.qin)
            print 'Peticion Recibida: \n' + json
            request = functions.fromJson(json)
            id = int(request['id'])
            if id == 1:
                response = classes.package('0001', '0000000', getAllFlights())
                response = functions.toPrettyJson(response)
                l = string.split(response)
                for s in l:
                    errno = cfunctions.mqsvSend(s, self.qout)
                    if errno != 0:
                        os.strerror(errno)       
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