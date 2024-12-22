import requests
from typing import List
url = "https://api.openbrewerydb.org/v1/breweries"
# sprawdzenie statusu
class Brewery:
    def __init__(self, id, name, street, city, state, postal_code, country, brewery_type):
        self.id = id
        self.name = name
        self.street = street
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.country = country
        self.brewery_type = brewery_type
    def __str__(self):
        return (f'Nazwa {self.name}, Ulica {self.street}, Miasto {self.city} \n'
                f'Wojewodztwo {self.state}, Kod pocztowy {self.postal_code}, Kraj {self.country}\n'
                f'Typ {self.brewery_type}')
def pobieranie_danych() -> List[Brewery]:
    #pobieranie
    pobieranie = requests.get(url, params={"Po stronie":20})
    pobieranie.raise_for_status()
    breweries_data = pobieranie.json()

    breweires = []
    for data in breweries_data:
        brewery = Brewery(
        id = data.get("id"),
        name = data.get("name"),
        brewery_type = data.get("brewery_type"),
        street = data.get("street"),
        city = data.get("city"),
        state = data.get("state"),
        postal_code = data.get("postal_code"),
        country = data.get("country"),

    )
    breweires.append(brewery)

    return breweires

def wydruk_danych():
    breweires = pobieranie_danych()
    for brewery in breweires:
        print(brewery)

if __name__ == "__main__":
    wydruk_danych()

