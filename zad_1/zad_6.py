# zad_6
def polacz_listy_i_poteguj(lista1, lista2):

    polaczona_lista = list(set(lista1 + lista2))

    wynik = [x ** 3 for x in polaczona_lista]

    return wynik
lista1 = [3, 3, 3, 3, 3]
lista2 = [3, 4, 5, 6, 7]
wynik = polacz_listy_i_poteguj(lista1, lista2)

print(wynik)