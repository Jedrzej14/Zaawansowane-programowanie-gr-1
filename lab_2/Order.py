class Order:
    def __init__(self, employee, student, Book, order_date):
        self.employee = employee
        self.student = student
        self.Book = Book
        self.order_date = order_date
    def __str__(self):
        def __str__(self):
            return f'Pracownik z {self.employee} drzwiami w kolorze'