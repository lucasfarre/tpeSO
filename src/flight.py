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

class Aircraft:
	id = 0
	model = ""
	seats = 0
	
	def __init__(self, id, model, seats):
		self.id = id
		self.model = model
		self.seats = seats

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
	
	