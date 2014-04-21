# from abc import ABCMeta
import dbback
import classes
import cfunctions
import socket
import functions
import time

class Client:
#     __metaclass__ = ABCMeta
    
    def __init__(self, ip, port):
        self.__ip = ip
        self.__port = port
    
    def open(self):
        ip = socket.gethostbyname(socket.gethostname())
        self.clientfd = cfunctions.clientInit(self.__ip, int(self.__port))
    
    def close(self):
        cfunctions.clientDown(self.clientfd)
    
    def connect(self):
        pass
    
    def disconnect(self):  
        pass
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toJson(header)
        cfunctions.writen(self.clientfd, header, 60)
        json = cfunctions.readn(self.clientfd, 60)[1]
        if len(json) >= 60:
            json = json[:60]
            header = functions.fromJson(json)
            length = int(header['length'])
            json = cfunctions.readn(self.clientfd, length)[1]
            if len(json) >= length:
                json = json[:length]
                print 'Response: \n' + json
                response = functions.fromJson(json)
        self.close()

ip = raw_input('Ingrese el IP del servidor: ')
port = raw_input('Ingrese el puerto del servidor: ')
s = Client(ip, port)
id = raw_input('Ingrese el ID de la peticion: ')
s.request(id)        
        
        
        
        
        