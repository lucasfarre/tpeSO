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
        self.mem = cfunctions.getmemPosix()
        self.sd = cfunctions.initmutexPosix()
        print str(self.mem)
        print str(self.sd)
    
    def request(self, id):
        self.open()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', time.time())
        header = functions.toJson(header)
        cfunctions.memwrite(self.mem, header)
        cfunctions.sempost(self.sd)
        cfunctions.semwait(self.sd)
        json = cfunctions.memread(self.mem)
        print json        
        cfunctions.sempost(self.sd)

def main():
    s = Client()
    id = raw_input('Ingrese el ID de la peticion: ')
    s.request(id)          
        
if __name__ == "__main__":
    main()        