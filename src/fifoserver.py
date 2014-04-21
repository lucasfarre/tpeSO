import gserver
import cfunctions
import os
import functions
import classes
import dbback

class FifoServer(gserver.Server):
    
    def __init__(self):
        self.name = '/tmp/fifo'
    
    def create(self):
        cfunctions.mkfifo(self.name, 0666)
        cfunctions.mkfifo('/tmp/fiforequest', 0666)
        cfunctions.mkfifo('/tmp/fiforesponse', 0666)
        
        self.fdresponse = os.open('/tmp/fiforesponse', os.O_WRONLY)
        self.fdrequest = os.open('/tmp/fiforequest', os.O_RDONLY)
    
    def close(self, fd):
        os.close(fd)
    
    def open(self, mode):
#         os.remove(self.name)
#         cfunctions.mkfifo(self.name, 0666)
        if mode == os.O_WRONLY:
            self.fdresponse = os.open('/tmp/fiforesponse', mode)
        else:
            self.fdrequest = os.open('/tmp/fiforequest', mode)
    
    def run(self):
        up = True
        self.create()
        while up == True:
            open = True
#             self.open(os.O_RDONLY)
#             cfunctions.lock(self.fd)
            json = cfunctions.readn(self.fdrequest, 60)[1]
#             cfunctions.unlock(self.fd)
#             self.close(self.fdrequest)
            if len(json) >= 60:
                json = json[:60]
                print 'Request received: \n' + json
                request = functions.fromJson(json)
                id = int(request['id'])
                if id == 0:
                    open = False
                    r = None
                if id == 1:
                    response = classes.package('0001', '0000000', dbback.getAllFlights())
                    response = functions.toJson(response)
                    length = str(len(response)).zfill(7)
                    response = classes.package('0001', '0000000', dbback.getAllFlights())
                    response = functions.toJson(response)
                    
                    header = classes.package('0001', length, None)
                    header = functions.toJson(header)
#                     self.open(os.O_WRONLY)
#                     cfunctions.lock(self.fd)
                    if cfunctions.writen(self.fdresponse, header, 60) != -1:
                        print 'Header sent: \n' + header
#                     cfunctions.unlock(self.fd)
#                     self.close(self.fdresponse)
#                     self.open(os.O_WRONLY)
#                     cfunctions.lock(self.fd)
                    cfunctions.writen(self.fdresponse, response, int(length))
#                     cfunctions.unlock(self.fd)
#                     self.close(self.fdresponse)
                if id == 2:
                    pass
                
def main():
    print 'Server'
    h = FifoServer()
    h.run()      
        
if __name__ == "__main__":
    main()