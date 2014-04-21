# from abc import ABCMeta
import dbback
import classes
import cfunctions
import socket
import functions

class Server:
#     __metaclass__ = ABCMeta

    def open(self):
        self.mem = cfunctions.getmem()
        print 'malloquie en ' + str(self.mem)
        cfunctions.memset(self.mem, 0, 10000)

    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            open = True
            json = cfunctions.memread(self.mem)
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
                    if cfunctions.memwrite(self.mem, header) != -1:
                        print 'Header sent: \n' + header
                    raw_input('prompt')
                    cfunctions.memwrite(self.mem, response)
                if id == 2:
                    pass
                
            raw_input('prompt')
#                 self.disconnect()
#         self.close()
        
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()
        
        
        
        