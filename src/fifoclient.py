import gclient
import cfunctions
import os
import classes
import functions
import time

class FifoClient(gclient.Client):
    
    def __init__(self):
        self.name = '/tmp/fifo'
        
    def close(self, fd):
        os.close(fd)
    
    def connect(self):
        self.clientfdresponse = os.open('/tmp/fiforesponse', os.O_RDONLY)
        self.clientfdrequest = os.open('/tmp/fiforequest', os.O_WRONLY)
    
    def disconnect(self):  
        pass
    
    def open(self, mode):
#         self.clientfd = os.open(self.name, mode)
        if mode == os.O_RDONLY:
            self.clientfdresponse = os.open('/tmp/fiforesponse', mode)
        else:
            self.clientfdrequest = os.open('/tmp/fiforequest', mode)
    
    def request(self, id):
        self.connect()
        id = int(id)
        header = classes.package(str(id).zfill(4), '0000060', None)
        header = functions.toJson(header)
#         self.open(os.O_WRONLY)
#         cfunctions.lock(self.clientfd)
        cfunctions.writen(self.clientfdrequest, header, 60)
#         cfunctions.unlock(self.clientfd)
#         self.close(self.clientfdrequest)
#         self.open(os.O_RDONLY)
#         cfunctions.lock(self.clientfd)
        json = cfunctions.readn(self.clientfdresponse, 60)[1]
#         cfunctions.unlock(self.clientfd)
#         self.close(self.clientfdresponse)
        if len(json) >= 60:
            json = json[:60]
            print json
            header = functions.fromJson(json)
            length = int(header['length'])
            print 'Abro'
#             self.open(os.O_RDONLY)
#             cfunctions.lock(self.clientfd)
            print 'Abrido'
            print 'Entro'
            json = cfunctions.readn(self.clientfdresponse, length)[1]
            print 'Salgo'
#             cfunctions.unlock(self.clientfd)
#             self.close(self.clientfdresponse)
            if len(json) >= length:
                json = json[:length]
                print 'Response: \n' + json
                response = functions.fromJson(json)
                
        ##### PETITION SALIR CLOSE

def main():
    print 'Client'
    s = FifoClient()
    id = raw_input('Ingrese el ID de la peticion: ')
    s.request(id)  
        
if __name__ == "__main__":
    main()