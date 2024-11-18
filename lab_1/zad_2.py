# %% A)
def wyswietl_imiona(imiona):
    for imie in imiona:
        print(imie)
# Przykład użycia
lista_imion = ['Anna', 'Jan', 'Michał', 'Kasia', 'Piotr']
wyswietl_imiona(lista_imion)


# %% B)
def pomnoz_przez_dwa(lista):
    return [liczba * 2 for liczba in lista]

liczby = [1, 2, 3, 4, 5]
wynik = pomnoz_przez_dwa(liczby)
print(wynik)



# %% C_
def pokaz_parzyste(numbers):
    for liczby in numbers:
        if liczby % 2 == 0:
            print(liczby)
numbers = range (10)
print((pokaz_parzyste(numbers)))

# %% D)
def _wpisz_co_druga(liczby):
    for i in range (0, len(liczby), 2 ):
        print(i)
liczby = range (10)
print(_wpisz_co_druga(liczby))

