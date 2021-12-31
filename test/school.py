class Person:
	name: str
	surname: str
	age: int
	id: int
	address: str
	friends: list["Person"]

	def walk(self):
		...

	def eat(self, food, amount: int):
		...

	def sleep(self):
		...


class Student(Person):
	grade: int
	student_id: int

	def study(self):
		...


class Staff(Person):
	position: str
	salary: float

	def work(self, essay):
		...


class Teacher(Staff):
	carreer: str
	subjects: list[str]

	def teach(self):
		...


class Administrator(Staff):
	def manage(self):
		...

	def audit(self):
		...


class Director(Administrator):
	def plan(self):
		...


class Class:
	name: str
	teacher: Teacher
	students: list[Student]
