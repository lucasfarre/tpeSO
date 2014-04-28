# -'- coding: iso8859-1 -'-

from dbback import *
import classes
import cfunctions
import socket
import functions

####################################################################################################
##### SRV Socket Server v2.0
##### Ejercicio 2.b
####################################################################################################

class Server:

    def open(self):
        ip = socket.gethostbyname(socket.gethostname())
        print 'IP: ' + ip
        print 'Puerto: 8889'
        r = cfunctions.serverInit("Test")
        self.fd = r['socket_fd']
        self.name = r['socket_name']
    
    def close(self):
        cfunctions.serverDown(self.fd, self.name)
    
    def connect(self):
        self.clientfd = cfunctions.serverConnect(self.fd)
    
    def disconnect(self):  
        cfunctions.serverDisconnect(self.clientfd)
    
    def makeResponseWithHeader(self,id,data):
        response = classes.package(id, '0000000', data)
        response = functions.toJson(response)
        length = str(len(response)).zfill(7)
        response = classes.package(id, '0000000', data)
        response = functions.toJson(response)   
        header = classes.package(id, length, None)
        header = functions.toPrettyJson(header)
        return {'header':header, 'length':int(length),'response':response };
    
    def SocketGetAllFlights(self):
        dic = self.makeResponseWithHeader('0001', getAllFlights())
        if cfunctions.writen(self.clientfd, dic['header'], 60) != -1:
            print 'Header sent: \n' + dic['header']
        cfunctions.writen(self.clientfd,  dic['response'], dic['length'])
        
    def run(self):
        if self.fd == -1:
            self.open()
        up = True
        while up == True:
            if self.clientfd == -1:
                self.connect()
            open = True
            json = cfunctions.readn(self.clientfd, 60)[1]
            if len(json) >= 60:
                json = json[:60]
                print 'Request received: \n' + json
                request = functions.fromJson(json)
                id = int(request['id'])
                if id == 1: 
                    self.SocketGetAllFlights()
                if id == 2: 
                    json = cfunctions.readn(self.clientfd, int(request['length']))[1]
                    json = json[:int(request['length'])]
                    json = functions.fromJson(json)
                    checkIn(json['data'],json['passenger'],json['seat'])
                if id == 3:
                    json = cfunctions.readn(self.clientfd, int(request['length']))[1]
                    json = json[:int(request['length'])]
                    json = functions.fromJson(json)
                    addFlight(json['data'])
                if id == 4: 
                    json = cfunctions.readn(self.clientfd, int(request['length']))[1]
                    json = json[:int(request['length'])]
                    json = functions.fromJson(json)
                    removeFlight(json['data'])
                if id == 6:
                    self.disconnect()
                    self.clientfd = -1

    def create(self):
       self.fd = -1
       self.clientfd = -1
        
def main():
    s = Server()
    s.create()
    s.run() 

if __name__ == "__main__":
    main()
