# Tworzenie bibliotek
from lab_2.Employee import Employee
from lab_2.Library import Library
from lab_2.Book import Book
from lab_2.Order import Order

library1 = Library("Warszawa", "Ulica 1", "00-001", "8:00-18:00", "123-456-789")
library2 = Library("Kraków", "Ulica 2", "00-002", "9:00-17:00", "987-654-321")

# Tworzenie pracowników
employee1 = Employee("Jan", "Kowalski", "2020-01-01", "1985-05-05", "Warszawa", "Ulica 1", "00-001", "123-456-789")
employee2 = Employee("Anna", "Nowak", "2019-02-01", "1988-06-06", "Kraków", "Ulica 2", "00-002", "987-654-321")
employee3 = Employee("Paweł", "Wiśniewski", "2021-03-01", "1990-07-07", "Warszawa", "Ulica 3", "00-003", "111-222-333")

# Tworzenie książek
book1 = Book(library1, "2010-01-01", "Adam", "Mickiewicz", 300)
book2 = Book(library2, "2015-02-02", "Henryk", "Sienkiewicz", 500)
book3 = Book(library1, "2020-03-03", "Juliusz", "Słowacki", 400)
book4 = Book(library2, "2018-04-04", "Bolesław", "Prus", 350)
book5 = Book(library1, "2022-05-05", "Stanisław", "Lem", 450)


# Tworzenie studentów (musimy stworzyć też klasę Student)
class Student:
    def __init__(self, first_name, last_name, student_id):
        self.first_name = first_name
        self.last_name = last_name
        self.student_id = student_id

    def __str__(self):
        return f"{self.first_name} {self.last_name}, ID: {self.student_id}"


student1 = Student("Piotr", "Kozłowski", "S123")
student2 = Student("Maria", "Wiśniewska", "S456")
student3 = Student("Krzysztof", "Zieliński", "S789")

# Tworzenie zamówień
order1 = Order(employee1, student1, [book1, book2], "2025-01-01")
order2 = Order(employee2, student2, [book3, book4, book5], "2025-02-01")

# Wydrukowanie zamówień
print(order1)
print(order2)
