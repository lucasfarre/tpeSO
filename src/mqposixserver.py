# from abc import ABCMeta
import dbback
import classes
import cfunctions
import socket
import functions
import os
import time
import string

class Server:
#     __metaclass__ = ABCMeta

    def open(self):
        self.qin = '/var/tmp/qin'
        self.qout = '/var/tmp/qout'
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            open = True
            
            json = 0
            while not isinstance(json, str):
                json = cfunctions.mqposixReceive(self.qin)
            
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

                    
#                     if cfunctions.memwrite(self.mem, header) != -1:
#                         print 'Header sent: \n' + header
#                     step = 1000
#                     for i in range(0, len(response), 1000):
#                         slice = response[i:step]
#                         print slice
#                         step += 1000
#                         errno = cfunctions.mqsvSend(slice, self.qout)
# #                         time.sleep(1)
#                         if errno != 0:
#                             os.strerror(errno)
                    l = string.split(response)
                    for s in l:
                        print s
                        errno = cfunctions.mqposixSend(s, self.qout)
                        if errno != 0:
                            os.strerror(errno)       
                    print 'mande'
#                     print 'enviando...'
#                     print os.strerror(cfunctions.mqsvSend(response, self.qout))
#                     print 'envie response'

                if id == 2:
                    pass   
#                 self.disconnect()
#         self.close()
        
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()
        
        
        
        