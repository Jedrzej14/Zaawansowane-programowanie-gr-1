import cv2 as cv
import os
import base64
import pika
from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()

# Ścieżki do modelu i pliku konfiguracyjnego
model_path = "ssd_mobilenet_v1_coco_2017_11_17.pb"
config_path = "ssd_mobilenet_v1_coco_2017_11_17.pbtxt"

# Wczytanie modelu
cvNet = cv.dnn.readNetFromTensorflow(model_path, config_path)

# Klasa reprezentująca osobę w COCO (ID=1)
PERSON_CLASS_ID = 1

# Parametry RabbitMQ
rabbitmq_host = "localhost"
QUEUE_NAME = "images_queue"

# Ustawienie połączenia RabbitMQ
try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
except Exception as e:
    print("Błąd połączenia z RabbitMQ:", str(e))
    connection = None


# Funkcja do wykrywania osób na obrazie
def detect_people(image_path):
    img = cv.imread(image_path)
    if img is None:
        return 0
    rows, cols, _ = img.shape

    # Przetwarzanie obrazu przez sieć neuronową
    blob = cv.dnn.blobFromImage(img, size=(300, 300), swapRB=True, crop=False)
    cvNet.setInput(blob)
    cvOut = cvNet.forward()

    person_count = 0
    for detection in cvOut[0, 0, :, :]:
        score = float(detection[2])
        class_id = int(detection[1])

        if class_id == PERSON_CLASS_ID and score > 0.3:
            # Zaznaczanie osoby na obrazie (np. rysowanie prostokąta)
            left = int(detection[3] * cols)
            top = int(detection[4] * rows)
            right = int(detection[5] * cols)
            bottom = int(detection[6] * rows)

            # Rysowanie prostokąta wokół osoby
            cv.rectangle(img, (left, top), (right, bottom), (0, 255, 0), 2)
            person_count += 1

    # Zapisz zmodyfikowany obraz w folderze saved_images
    saved_image_path = "saved_images/" + os.path.basename(image_path)
    cv.imwrite(saved_image_path, img)  # Zapisanie obrazu po detekcji

    return person_count, saved_image_path

@app.get("/")
def hello_world():
    return "Witaj, w detekcji zdjęć!"

#zdjecie
@app.get("/detect_people")
def detect_people_from_local_image(image_path: str = "D:\\studia\\Kurspython\\Detekcja_zdjec_projekt\\1.jpg"):
    try:
        person_count = detect_people(image_path)
        return {"detected_people": person_count}
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd serwera: {str(e)}")

# kolejkowanie
@app.get("/queue_and_detect_images")
def queue_and_detect_images(folder_path: str = "D:\\studia\\Kurspython\\Detekcja_zdjec_projekt\\test_image"):
    # Sprawdzenie, czy folder istnieje
    if not os.path.exists(folder_path) or not os.path.isdir(folder_path):
        raise HTTPException(status_code=400, detail="Podany folder nie istnieje lub nie jest folderem.")

    images_queued = []
    results = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(folder_path, filename)

            try:
                # Wykonaj detekcję na obrazie
                person_count, saved_image_path = detect_people(image_path)

                # Zakolejkowanie obrazu (zakładając, że RabbitMQ jest już skonfigurowane)
                with open(saved_image_path, "rb") as image_file:
                    image_data = image_file.read()
                    encoded_image = base64.b64encode(image_data).decode("utf-8")

                # Wysłanie obrazu do kolejki RabbitMQ
                channel.basic_publish(exchange="", routing_key=QUEUE_NAME, body=encoded_image)

                images_queued.append(filename)
                results.append({
                    "filename": filename,
                    "detected_people": person_count,
                    "saved_image_path": saved_image_path
                })

            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Błąd podczas przetwarzania pliku {filename}: {str(e)}")

    return {"results": results}


# url

url_detection_folder = "url_przed_detekcja"
if not os.path.exists(url_detection_folder):
    os.makedirs(url_detection_folder)


def download_image_from_url(image_url: str) -> str:
    try:
        response = requests.get(image_url, stream=True)
        if response.status_code != 200:
            raise HTTPException(status_code=400, detail=f"Nie udało się pobrać obrazu z URL: {image_url}")

        # Nazwa pliku (na podstawie URL)
        filename = os.path.basename(image_url.split("?")[0])  # Ignorujemy parametry w URL
        local_path = os.path.join(url_detection_folder, filename)

        # Zapisujemy obraz lokalnie
        with open(local_path, "wb") as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        return local_path
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd podczas pobierania obrazu z URL: {str(e)}")


# Endpoint do detekcji osób na obrazie z URL
@app.get("/detect_people_from_url")
def detect_people_from_url(image_url: str):
    """
    Endpoint przyjmuje URL obrazu, wykrywa osoby i zwraca wynik w formacie JSON.
    """
    try:
        # Pobierz obraz z URL i zapisz lokalnie (przed detekcją)
        local_image_path = download_image_from_url(image_url)

        # Wykonaj detekcję osób na obrazie (zapisuje obraz w "saved_images")
        person_count, saved_image_path = detect_people(local_image_path)

        # Przenieś obraz po detekcji do folderu "url_po_detekcji"
        url_detection_folder = "url_po_detekcji"
        if not os.path.exists(url_detection_folder):
            os.makedirs(url_detection_folder)

        # Nowa ścieżka dla obrazu
        new_image_path = os.path.join(url_detection_folder, os.path.basename(saved_image_path))
        os.rename(saved_image_path, new_image_path)  # Przeniesienie pliku

        # Zwróć wynik w formacie JSON
        return {
            "url": image_url,
            "detected_people": person_count,
            "saved_image_path": new_image_path
        }
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Błąd serwera: {str(e)}")