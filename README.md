# Pymaid

Create Mermaid representations from python code.


## Example

This python code:

```py
class Person:
	name: str
	surname: str
	age: int
	id_: int
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
```

#### `pymaid file.py class` would generate the following mermaid class diagram:


```mermaid
classDiagram
direction TB
class Person {
	str: name
	str: surname
	int: age
	int: id_
	str: address
	list['Person']: friends
	eat(self, food, amount) None
	sleep(self) None
	walk(self) None
}
object <|-- Person
class object
class Staff {
	str: position
	float: salary
	eat(self, food, amount) None
	sleep(self) None
	walk(self) None
	work(self, essay) None
}
Person <|-- Staff
class Student {
	int: grade
	int: student_id
	eat(self, food, amount) None
	sleep(self) None
	study(self) None
	walk(self) None
}
Person <|-- Student
class Teacher {
	str: carreer
	list[str]: subjects
	eat(self, food, amount) None
	sleep(self) None
	teach(self) None
	walk(self) None
	work(self, essay) None
}
Staff <|-- Teacher
```

Several command arguments are available for altering the generated diagram.