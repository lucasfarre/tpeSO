import dbback
import classes
import cfunctions
import socket
import functions
import time

class Client():
    
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
        cfunctions.down(self.semid, 1)
        cfunctions.memwrite(self.mem, header)
        cfunctions.up(self.semid, 2)        
        cfunctions.down(self.semid, 3)
        json = cfunctions.memread(self.mem)
        print json
        cfunctions.up(self.semid, 1)

def main():
    s = Client()
    id = raw_input('Ingrese el ID de la peticion: ')
    s.request(id)          
        
if __name__ == "__main__":
    main()