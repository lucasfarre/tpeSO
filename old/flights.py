from functions import *
from demo import printf, lock1 #@UnresolvedImport
import json


# user = raw_input("user: ")
# password = raw_input("password: ")

passenger = Passenger(0, "Lucas", "ARG", "92-")
seats = []
for i in range(1, 30):
    for j in list("ABCDEF"):
        seats.append(Seat(i, j, False, None))
aircraft = Aircraft(0, "Airbus A320", seats)
flight = Flight(0, "12/12/12", "13/12/12", "EZE", "JFK", True, aircraft)

flights = []
flights.append(flight)

j = toJson(flights)
flight2 = fromJson(j)
print(flight2)
j = toJson(jsonObjectAsDict(flight2))
print(j)
# lock1()ij7uhy6t5r

