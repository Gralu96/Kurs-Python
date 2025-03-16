# Używamy oficjalnego obrazu Pythona
FROM python:3.11-slim

# Ustawiamy katalog roboczy w kontenerze
WORKDIR /app

# Kopiujemy pliki z zależnościami
COPY requirements.txt .

# Instalujemy zależności
RUN pip install --no-cache-dir -r requirements.txt

# Kopiujemy pliki aplikacji
COPY main.py .
COPY websocket_server.py .
COPY front-init/ front-init/

# Tworzymy katalog na dane
RUN mkdir -p storage

# Definiujemy volume dla przechowywania danych
VOLUME ["/app/storage"]

# Eksponujemy porty
EXPOSE 3000 5000

# Uruchamiamy oba serwery przy pomocy supervisord
RUN pip install supervisor

# Konfiguracja supervisord
COPY supervisord.conf .

# Uruchamiamy supervisord
CMD ["supervisord", "-c", "supervisord.conf"]
