# from abc import ABCMeta
import dbback
import classes
import cfunctions
import socket
import functions

class Server:
#     __metaclass__ = ABCMeta

    def open(self):
        self.mem = cfunctions.getmemPosix()
#        print 'malloquie en ' + str(self.mem)
#        cfunctions.memset(self.mem, 0, 10000)
        self.sd = cfunctions.initmutexPosix()
        print str(self.mem)
        print str(self.sd)
    
    def run(self):
        self.open()
        up = 1
        while up == 1:
            open = True
            
#            print('Down 2')
#            cfunctions.down(self.semid, 2)
            cfunctions.semwait(self.sd)
            json = cfunctions.memread(self.mem)
            
            if len(json) >= 60:
#                 json = json[:60]
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
                    cfunctions.sempost(self.sd)
                    cfunctions.memwrite(self.mem, response)
#                    cfunctions.up(self.semid, 3)
                    cfunctions.semwait(self.sd)
                    #print 'up del 3: '
                    break

                if id == 2:
                    pass   
#                 self.disconnect()
#         self.close()
        
def main():
    s = Server()
    s.run()        
        
if __name__ == "__main__":
    main()