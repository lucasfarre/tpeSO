class Passenger:
	id = 0
	name = ""
	nationality = ""
	birthday = 0
	
	def __init__(self, id, name, nationality, birthday):
		self.id = id
		self.name = name
		self.nationality = nationality
		self.birthday = birthday
		
	def from_dict(dct):
		if '__type__' in dct and dct['__type__'] == 'Passenger':
			return Passenger(dct['id'], dct['name'], dct['nationality'], dct['birthday'])
		return dct

class Seat:
	row = 1
	column = "A"
	status = False
	passenger = 0
	
	def __init__(self, row, column, status, passenger):
		self.row = row
		self.column = column
		self.status = status
		self.passenger = passenger
	
	def from_dict(dct):
		if '__type__' in dct and dct['__type__'] == 'Seat':
			return Seat(dct['row'], dct['column'], dct['status'], as_passenger(dct['passenger']))
		return dct


class Aircraft:
	id = 0
	model = ""
	seats = 0
	
	def __init__(self, id, model, seats):
		self.id = id
		self.model = model
		self.seats = seats
	
	def from_dict(dct):
		if '__type__' in dct and dct['__type__'] == 'Aircraft':
			return Aircraft(dct['id'], dct['model'], dct['seats'], [as_seat(dct['passenger'])])
		return dct

class Flight:
	id = 0
	departDate = 0
	arriveDate = 0
	departAirport = ""
	arriveAirport = ""
	status = False
	aircraft = 0
	
	def __init__(self, id, departDate, arriveDate, departAirport, arriveAirport, status, aircraft):
		self.id = id
		self.departDate = departDate
		self.arriveDate = arriveDate
		self.departAirport = departAirport
		self.arriveAirport = arriveAirport
		self.status = status
		self.aircraft = aircraft

	def from_dict(dct):
		if '__type__' in dct and dct['__type__'] == 'Flight':
			return Flight(dct['id'], dct['departDate'], dct['arriveDate'], dct['departAirport'], dct['arriveAirport'], dct['status'], as_aircraft(dct['aircraft']))
		return dct
	






	
	