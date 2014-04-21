# from abc import ABCMeta
import dbback
import classes
import cfunctions
import socket
import functions
import time

class Client():
#     __metaclass__ = ABCMeta
    
    def __init__(self):
        pass
    
    def open(self):
        self.mem = cfunctions.getmem()
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toJson(header)
        cfunctions.memwrite(self.mem, header)
        raw_input('prompt')
        json = cfunctions.memread(self.mem)
        if len(json) >= 60:
            json = json[:60]
            header = functions.fromJson(json)
            length = int(header['length'])
            raw_input('prompt')
            json = cfunctions.memread(self.mem)
            if len(json) >= length:
                json = json[:length]
                print 'Response: \n' + json
                response = functions.fromJson(json)
#         self.close()     
        
def main():
#     ip = raw_input('Ingrese el IP del servidor: ')
#     port = raw_input('Ingrese el puerto del servidor: ')
    s = Client()
    id = raw_input('Ingrese el ID de la peticion: ')
    s.request(id)          
        
if __name__ == "__main__":
    main()
        
        
        
        