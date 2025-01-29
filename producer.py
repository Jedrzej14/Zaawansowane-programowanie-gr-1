import csv
import time
import uuid


def add_task(filename="tasks.tst"):
    """Dodaje nowe zadanie do pliku CSV."""
    task_id = str(uuid.uuid4())
    status = "pending"

    with open(filename, mode="a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([task_id, status])

    print(f"Dodano zadanie: {task_id} (status: {status})")


if __name__ == "__main__":
    while True:
        add_task()
        time.sleep(5)  # Producent dodaje nowe zadanie co 5 sekund
