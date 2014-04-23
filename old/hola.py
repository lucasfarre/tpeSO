import cfunctions
import os
import string
import time

name = '/tmp/fifo'
print name
cfunctions.mkfifo(name, 0666)
# cfunctions.signal()

# while True:
# f = open('db.json', 'r')
# s = f.read()
# for w in string.split(s):
#     time.sleep(0.01)
#     fd = os.open(name, os.O_WRONLY)
#     #cfunctions.write(fd, w, len(w))
#     os.write(fd, w)
#     os.close(fd)


f = open('db.json', 'r')
s = f.read()
print str(len(s))
fd = os.open(name, os.O_WRONLY)
# cfunctions.write(fd, s, len(s))
cfunctions.writen(fd, s, len(s))
os.close(fd)