class Passenger:
    def __init__(self, id, name, nationality, birthday):
        self.id = id
        self.name = name
        self.nationality = nationality
        self.birthday = birthday

def as_passenger(dct):
        if '__type__' in dct and dct['__type__'] == 'Passenger':
            return Passenger(dct['id'], dct['name'], dct['nationality'], dct['birthday'])
        return dct

from functions import *
from classes import *
import json
from collections import namedtuple

    
p = newPassenger(12345678, 'Pepe', 'USA', '12-12-1990')
ps = []
ps.append(p)
ps.append(p)
ps.append(p)



j = toJson(ps)

# j[0] = Passenger(12345678, 'Jojose', 'USA', '12-12-1990')

q = fromJson(j)
# for p in q:
#     print(p.id)
#     print(p.nationality)
# print(toJson(q))
print(toJson(q))


