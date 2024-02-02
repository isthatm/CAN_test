from datetime import date

# random Person
class Person:
    def __init__(self, name, age, number):
        self.name = name
        self.age = age
        self.random_number = number

    @classmethod
    def fromBirthYear(cls, name, birthYear, number):
        return cls(name, date.today().year - birthYear, number)

    def display(self):
        print(self.name + "'s age is: " + str(self.age) + "; " +str(self.random_number))

person = Person('Adam', 19, 20)
person.display()

person1 = Person.fromBirthYear('John',  1985, 40)
person1.display()