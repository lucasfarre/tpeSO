def newPassenger(id, name, nationality, birthday):
    return {'id': id, 
            'name': name, 
            'nationality': nationality, 
            'birthday': birthday}

def newSeat(row, column, passenger, status):
    return {'row': row, 
            'column': column, 
            'passenger': passenger, 
            'status': status}

def newAircraft(id, model, seats, seatsRows, seatsColumns):
    return {'id': id, 
            'model': model, 
            'seats': seats, 
            'seatsRows': seatsRows, 
            'seatsColumns': seatsColumns}

def newFlight(id, departDate, departAirport, arriveDate, arriveAirport, status, aircraft):
    return {'id': id, 
            'departDate': departDate, 
            'departAirport': departAirport, 
            'arriveDate': arriveDate, 
            'arriveAirport': arriveAirport, 
            'status': status, 
            'aircraft': aircraft}
    
def socketPackage(id, pid, data, ip, port):
    return {'id': id,
            'pid': pid,
            'data': data,
            'ip':ip,
            'port': port}
    
def newPetitionMsg(id,pid,data,passenger,seat):
    return {'id': id,
            'pid': pid,
            'data':data,
            'passenger':passenger,
            'seat':seat}
    
def package(id, length, data):
    return {'id': id,
            'length': length,
            'data': data}