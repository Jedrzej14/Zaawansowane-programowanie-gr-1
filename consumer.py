import csv
import time


def process_tasks(filename="tasks.txt"):
    """Przetwarza zadania z pliku CSV."""
    while True:
        tasks = []
        updated = False

        with open(filename, mode="r", newline="") as file:
            reader = csv.reader(file)
            for row in reader:
                if row[1] == "pending" and not updated:
                    print(f"Przetwarzanie zadania: {row[0]}")
                    row[1] = "in_progress"
                    updated = True
                tasks.append(row)

        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(tasks)

        time.sleep(5)  # Konsument sprawdza plik co 5 sekund


if __name__ == "__main__":
    process_tasks()
