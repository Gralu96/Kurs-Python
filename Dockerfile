# Używamy Alpine Linux z Pythonem - to najbardziej minimalny obraz (~50MB)
FROM python:3.13-alpine

# Ustawiamy katalog roboczy
WORKDIR /app

# Kopiujemy tylko plik aplikacji
COPY asystent_osobisty.py .

# Uruchamiamy aplikację
CMD ["python", "asystent_osobisty.py"]
