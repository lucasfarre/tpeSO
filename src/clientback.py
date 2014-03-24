from functions import fromJson, toJson

def flightStatus(flight):
    f = open("db.json", "r+")
    flightsString = f.read()
    flights = fromJson(flightsString)
    print(flights[0].get("aircraft").get("model"))
    flights[0]["aircraft"]["model"] = "Boeing 777"
    updated = toJson(flights)
    f.seek(0)
    f.truncate()
    f.write(updated)
    f.close()