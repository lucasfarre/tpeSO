# -'- coding: iso8859-1 -'-

from classes import *
from functions import *
import cfunctions
import os

####################################################################################################
##### SRV Database Manager Back v2.0
##### Común para todas las implementaciones
####################################################################################################

databaseFileName = 'srv.json'

def getAllFlights():
    fd = open(databaseFileName, 'r')
    db = fd.read()
    flights = fromJson(db)
    fd.close()
    return flights

def checkIn(flightId, passenger, seat):
    fd = open(databaseFileName, 'r+')
    cfunctions.lock(fd.fileno())
    db = fd.read()
    flights = fromJson(db)
    for flight in flights:
        if flight['id'] == flightId:
            for s in flight['aircraft']['seats']:
                if s['column'] == seat['column'] and s['row'] == seat['row']:
                    s['passenger'] = passenger
                    s['status'] = True
    updated = toJson(flights)
    reWrite(fd,updated)
    cfunctions.unlock(fd.fileno())
    fd.close()
    
def addFlight(flight):
    fd = open(databaseFileName, 'r+')
    db = fd.read()
    flights = fromJson(db)
    for f in flights :
       if f['id'] == flight['id'] :
           return None
    flights.append(flight)
    updated = toJson(flights)
    reWrite(fd,updated)
    fd.close()

def removeFlight(flightIndex):
    fd = open(databaseFileName, 'r+')
    db = fd.read()
    flights = fromJson(db)
    del flights[flightIndex]
    updated = toJson(flights)
    reWrite(fd,updated)
    fd.close()

def reWrite(fd,data):
    fd.seek(0)
    fd.truncate()
    fd.write(data)
    fd.flush()
    os.fsync(fd.fileno())