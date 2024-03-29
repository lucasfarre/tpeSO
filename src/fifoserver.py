# -'- coding: iso8859-1 -'-

import os
import cfunctions
import functions
import classes
from dbback import *

####################################################################################################
##### SRV Fifo Server v2.0
##### Ejercicio 2.a.3
####################################################################################################

class FifoServer:
    
    def create(self):
        cfunctions.mkfifo('/tmp/fiforequest', 0666)
        cfunctions.mkfifo('/tmp/fiforesponse', 0666)
        self.fdresponse = os.open('/tmp/fiforesponse', os.O_WRONLY)
        self.fdrequest = os.open('/tmp/fiforequest', os.O_RDONLY)
    
    def close(self, fd):
        os.close(fd)
    
    def open(self, mode):
        if mode == os.O_WRONLY:
            self.fdresponse = os.open('/tmp/fiforesponse', mode)
        else:
            self.fdrequest = os.open('/tmp/fiforequest', mode)
    
    def makeResponseWithHeader(self,id,data):
        response = classes.package(id, '0000000', data)
        response = functions.toJson(response)
        length = str(len(response)).zfill(7)
        response = classes.package(id, '0000000', data)
        response = functions.toJson(response)   
        header = classes.package(id, length, None)
        header = functions.toPrettyJson(header)
        return {'header':header, 'length':int(length),'response':response };
    
    def fifoGetAllFlights(self):
        dic = self.makeResponseWithHeader('0001', getAllFlights())
        if cfunctions.writen(self.fdresponse, dic['header'], 60) != -1:
            print 'Header sent: \n' + dic['header']
        cfunctions.writen(self.fdresponse,  dic['response'], dic['length'])
        
    def run(self):
        up = True
        self.create()
        while up == True:
            ok = False
            while not ok:
                json = cfunctions.readn(self.fdrequest, 60)[1]
                if len(json) >= 60:
                    json = json[:60]
                    try:
                        request = functions.fromJson(json)
                    except ValueError:
                        pass
                    else:
                        print 'Request received: \n' + json
                        ok = True
            id = int(request['id'])
            if id == 1: 
                self.fifoGetAllFlights()
            if id == 2: 
                json = cfunctions.readn(self.fdrequest, int(request['length']))[1]
                json = json[:int(request['length'])]
                json = functions.fromJson(json)
                checkIn(json['data'],json['passenger'],json['seat'])
            if id == 3:
                json = cfunctions.readn(self.fdrequest, int(request['length']))[1]
                json = json[:int(request['length'])]
                json = functions.fromJson(json)
                addFlight(json['data'])
            if id == 4: 
                json = cfunctions.readn(self.fdrequest, int(request['length']))[1]
                json = json[:int(request['length'])]
                json = functions.fromJson(json)
                removeFlight(json['data'])
        
def main():
    print 'Server'
    h = FifoServer()
    h.run()      
        
if __name__ == "__main__":
    main()
