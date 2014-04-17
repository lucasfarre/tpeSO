import cfunctions
import os

name = '/tmp/fifo'
print name
while True:
    fd = os.open(name, os.O_RDONLY)
#     print cfunctions.read(fd)
    print cfunctions.readn(fd, 68136)[1]
    os.close(fd)
#     
#     print cfunctions.fifoRead(name)

 #   print cfunctions.readn(fd, s, 68136)
