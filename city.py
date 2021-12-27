from school import Person

class City:
	buildings: list["Building"]
	people: list[Person]


class Building:
	name: str
	address: str
	floors: int
	rooms: int


class Family:
	children: list[Person]
	parents: list[Person]


class School(Building):
	classes: int
	teachers: list[Person]
	students: list[Person]


class University(School):
	faculties: int
	departments: int

class TownHall(Building):
	mayor: Person

	def announce(self, announcement):
		...

class Factory(Building):
	workers: list[Person]
	director: Person
	def produce(self):
		...
	def sell(self):
		...

class Vehicle:
	fuel: str
	engine: str
	seat: int
	brand: str
	model: str

class Car(Vehicle):
	doors: int
	wheels: int

class Plane(Vehicle):
	wings: int
	propellers: int
	def takeoff(self):
		...
	def land(self):
		...

class Ship(Vehicle):
	cargo: int
	def load(self, cargo):
		...
	def unload(self, cargo):
		...

class CarFactory(Factory):
	cars: list[Car]

class Home(Building):
	owner: Family
	garage: list[Vehicle]
