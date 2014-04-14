from cfunctions import *
import os

name = '/tmp/fifo'
print name
createFifo(name)
f = open(name, 'r+')
while True:
    print 'Leo del fifo: ' + f.read()