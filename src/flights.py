from flight import Passenger, Seat, Aircraft, Flight
from functions import toJson, fromJson
from demo import printf, lock1 #@UnresolvedImport

# user = raw_input("user: ")
# password = raw_input("password: ")

passenger = Passenger(0, "Lucas", "ARG", "92-")
seats = []
for i in range(1, 30):
    for j in list("ABCDEF"):
        seats.append(Seat(i, j, False, None))
aircraft = Aircraft(1, "Airbus A320", seats)
flight = Flight(1, "12/12/12", "13/12/12", "EZE", "JFK", True, aircraft)

flights = []
flights.append(flight)

j = toJson(flights)
flight2 = fromJson(j)
j = toJson(flight2)
printf(j)
lock1()
