import pytesseract
from PIL import Image

image_path = "example.jpg"
def read_text_from_image(image_path):
    """
    Odczytuje tekst ze zdjęcia za pomocą pytesseract.

    :param image_path: Ścieżka do pliku obrazu
    :return: Odczytany tekst
    """
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        return f"Błąd: {e}"


# Przykładowe użycie
  #
extracted_text = read_text_from_image(image_path)
print("📌 Odczytany tekst:\n", extracted_text)
