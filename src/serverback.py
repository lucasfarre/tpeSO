from functions import fromJson, toJson
from classes import *
import cfunctions
import os
 
def reWrite(fd,data):
    fd.seek(0)
    fd.truncate()
    fd.write(data)
    fd.flush()
    os.fsync(fd.fileno())
    
def flightStatus(flightId):
    fd = open("db.json", "r+")
    db = fd.read()
    flights = fromJson(db)
    for f in flights :
       if f["id"] ==  flightId :
           return f
    return None
    fd.close()
    
def addFlight(flight):
    fd = open("db.json", "r+")
    db = fd.read()
    flights = fromJson(db)
    for f in flights :
       if f["id"] == flight["id"] :
           return None
    flights.append(flight)
    updated = toJson(flights)
    reWrite(fd,updated)
    fd.close()
 
def checkIn(flightId, passenger, seat):
    fd = open("db.json", "r+")
    cfunctions.lock(fd.fileno())
    db = fd.read()
    flights = fromJson(db)
    for flight in flights:
        if flight["id"] == flightId:
            for s in flight["aircraft"]["seats"]:
                if s["column"] == seat['column'] and s["row"] == seat['row']:
                    s["passenger"] = passenger
                    s["status"] = True
    updated = toJson(flights)
    reWrite(fd,updated)
    cfunctions.unlock(fd.fileno())
    fd.close()
    
def modifyFlight(flight):
    fd = open("db.json", "r+")
    db = fd.read()
    flights = fromJson(db)
    for f in flights :
       if f["id"] ==  flight["id"] :
           flights.remove(f)
           flights.append(flight)
    updated = toJson(flights)
    reWrite(fd,updated)
    fd.close()
    
def removeFlight(flightId):
    fd = open("db.json", "r+")
    db = fd.read()
    flights = fromJson(db)
    for f in flights :
       if f["id"] == flightId :
           flights.remove(f);
    updated = toJson(flights)
    reWrite(fd,updated)
    fd.close()

def getAllFlights():
    fd = open("db.json", "r")
    db = fd.read()
    flights = fromJson(db)
    fd.close()
    return flights