from cfunctions import *
import os

name = '/tmp/fifo'
print name
createFifo(name)
print 'hola'
f = open(name, 'w+')
print 'hola'
s = raw_input('Escribir en el fifo: ')
f.write(s)