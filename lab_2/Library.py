class Library:
    def __init__(self, city, street, zip_code, open_hours, phone):
        self.city = city
        self.street = street
        self.zip_code = zip_code
        self.open_hour = open_hours
        self.phone = phone
    def __str__(self):
        return (f'Miasto{self.city}, Ulica{self.street}//'
                f'Kod pocztowy {self.zip_code}, Godziny otwarcia {self.open_hour}, Telefon {self.phone}')