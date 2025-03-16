import asyncio
import websockets
import json
from datetime import datetime
import pathlib

# Konfiguracja ścieżki do pliku data.json
STORAGE_DIR = pathlib.Path("storage")
DATA_FILE = STORAGE_DIR / "data.json"

# Upewniamy się, że folder storage istnieje
STORAGE_DIR.mkdir(exist_ok=True)

async def handle_websocket(websocket, path):
    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                username = data.get("username", "")
                message_content = data.get("message", "")
                
                timestamp = datetime.now().isoformat()
                
                # Wczytanie istniejących danych
                try:
                    with open(DATA_FILE, "r", encoding="utf-8") as f:
                        messages = json.load(f)
                except (json.JSONDecodeError, FileNotFoundError):
                    messages = {}
                
                # Dodanie nowej wiadomości
                messages[timestamp] = {
                    "username": username,
                    "message": message_content
                }
                
                # Zapisanie zaktualizowanych danych
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)
                
                # Wysłanie potwierdzenia
                await websocket.send(json.dumps({"status": "ok"}))
                
            except json.JSONDecodeError:
                await websocket.send(json.dumps({
                    "status": "error",
                    "message": "Nieprawidłowy format JSON"
                }))
                
    except websockets.exceptions.ConnectionClosed:
        pass

async def main():
    async with websockets.serve(handle_websocket, "localhost", 5000):
        print("Serwer WebSocket uruchomiony na ws://localhost:5000")
        await asyncio.Future()  # Działaj w nieskończoność

if __name__ == "__main__":
    asyncio.run(main())
