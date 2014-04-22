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
        self.semid = cfunctions.initmutex()
        print str(self.semid)
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', time.time())
        header = functions.toJson(header)
        print 'Down 1'
        cfunctions.down(self.semid, 1)
        print 'Sigo porque en seguida vuelve a 0'
        cfunctions.memwrite(self.mem, header)
        

        cfunctions.up(self.semid, 2)
        print 'up del 2: '
        
        cfunctions.down(self.semid, 3)
        print 'Down del 3: '

        json = cfunctions.memread(self.mem)
        print json
        cfunctions.up(self.semid, 1)
        print 'up del 1: '

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
        
        
        
        