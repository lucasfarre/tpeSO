from functions import fromJson, toJson

def flightStatus(flight):
    f = open("db.json", "r+")
    flightsString = f.read()
    flights = fromJson(flightsString)
    print(flights[0].get("aircraft").get("model"))
    flights[0]["aircraft"]["model"] = "Airbus A320"
    updated = toJson(flights)
    f.seek(0)
    f.truncate()
    f.write(updated)
    f.close()

def checkIn(flightId, passenger, seat):
    f = open("db.json", "r+")
    db = f.read()
    flights = fromJson(db)
    for flight in flights:
        if flight["id"] == flightId:
            for s in flight["aircraft"]["seats"]:
                if s["column"] == seat.column and s["row"] == seat.row:
                    s["passenger"] = passenger
                    s["status"] = True
    updated = toJson(flights)
    f.seek(0)
    f.truncate()
    f.write(updated)
    f.close()