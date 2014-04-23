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
        self.qin = '/qout'
        self.qout = '/qin'
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toJson(header)
        cfunctions.mqposixSend(header, self.qout)
        json = 0
        print 'Entro al while'
        e = True
        json = ''
        while e:
            try:
                s = cfunctions.mqposixReceive(self.qin)
                json = json + s
                response = functions.fromJson(json)
            except ValueError:
                pass
            else:
                e = False
        print functions.toJson(response)
#         if len(json) >= 60:
#             json = json[:60]
#             header = functions.fromJson(json)
#             length = int(header['length'])
#             cfunctions.down(self.semid, 0)
#             json = cfunctions.memread(self.mem)
#             cfunctions.up(self.semid, 0)
#             if len(json) >= length:
#                 json = json[:length]
#                 print 'Response: \n' + json
#                 response = functions.fromJson(json)
#         self.close()     
        
def main():
#     ip = raw_input('Ingrese el IP del servidor: ')
#     port = raw_input('Ingrese el puerto del servidor: ')
    s = Client()
    id = raw_input('Ingrese el ID de la peticion: ')
    s.request(id)          
        
if __name__ == "__main__":
    main()
        
        
        
        
