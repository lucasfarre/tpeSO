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

def newAircraft(id, model, seats):
    return {'id': id, 
            'model': model, 
            'seats': seats}

def newFlight(id, departDate, departAirport, arriveDate, arriveAirport, status, aircraft):
    return {'id': id, 
            'departDate': departDate, 
            'departAirport': departAirport, 
            'arriveDate': arriveDate, 
            'arriveAirport': arriveAirport, 
            'status': status, 
            'aircraft': aircraft}