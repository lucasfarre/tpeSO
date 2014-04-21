# from abc import ABCMeta
import dbback
import classes
import cfunctions
import socket
import functions

class Server:
#     __metaclass__ = ABCMeta
    
    def __init__(self):
        pass
    
    def open(self):
        ip = socket.gethostbyname(socket.gethostname())
        print 'IP: ' + ip
        r = cfunctions.serverInit("Test")
        self.fd = r['socket_fd']
        self.name = r['socket_name']
    
    def close(self):
        cfunctions.serverDown(self.fd, self.name)
    
    def connect(self):
        self.clientfd = cfunctions.serverConnect(self.fd)
    
    def disconnect(self):  
        cfunctions.serverDisconnect(self.clientfd)
    
    def run(self):
        self.open()
        up = True
        while up == True:
            self.connect()
            open = True
            json = cfunctions.readn(self.clientfd, 60)[1]
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
                    cfunctions.writen(self.clientfd, header, 60)
                    print 'Header sent: \n' + header
                    cfunctions.writen(self.clientfd, response, int(length))
                if id == 2:
                    pass
                self.disconnect()
        self.close()
        
s = Server()
s.run()        
        
        
        
        
        