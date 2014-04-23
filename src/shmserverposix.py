import dbback
import classes
import cfunctions
import socket
import functions

class Server:

    def open(self):
        self.mem = cfunctions.getmemPosix()
        self.sd = cfunctions.initmutexPosix()
        print str(self.mem)
        print str(self.sd)
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            open = True
            cfunctions.semwait(self.sd)
            json = cfunctions.memread(self.mem)
            
            if len(json) >= 60:
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
                    cfunctions.sempost(self.sd)
                    cfunctions.memwrite(self.mem, response)
                    cfunctions.semwait(self.sd)
                if id == 2:
                    pass   

def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()