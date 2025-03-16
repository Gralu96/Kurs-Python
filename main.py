from aiohttp import web
import aiohttp
import json
from datetime import datetime
import os
import pathlib
from aiohttp import WSMsgType

# Tworzenie folderu storage jeśli nie istnieje
storage_dir = pathlib.Path("storage")
storage_dir.mkdir(exist_ok=True)

# Ścieżka do pliku data.json
DATA_FILE = storage_dir / "data.json"

# Inicjalizacja pustego pliku JSON jeśli nie istnieje
if not DATA_FILE.exists():
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump({}, f, ensure_ascii=False, indent=2)

async def index(request):
    return web.FileResponse("front-init/index.html")

async def message_page(request):
    return web.FileResponse("front-init/message.html")

async def error_404(request):
    return web.FileResponse("front-init/error.html")

async def handle_message(request):
    if request.method == "POST":
        data = await request.post()
        username = data.get("username", "")
        message = data.get("message", "")
        
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
            "message": message
        }
        
        # Zapisanie zaktualizowanych danych
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(messages, f, ensure_ascii=False, indent=2)
        
        # Przekierowanie z powrotem na stronę wiadomości
        raise web.HTTPFound("/message.html")

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    
    async for msg in ws:
        if msg.type == WSMsgType.TEXT:
            try:
                data = json.loads(msg.data)
                username = data.get("username", "")
                message = data.get("message", "")
                
                timestamp = datetime.now().isoformat()
                
                # Wczytanie i aktualizacja danych
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    messages = json.load(f)
                
                messages[timestamp] = {
                    "username": username,
                    "message": message
                }
                
                with open(DATA_FILE, "w", encoding="utf-8") as f:
                    json.dump(messages, f, ensure_ascii=False, indent=2)
                
                # Wysłanie potwierdzenia
                await ws.send_json({"status": "ok"})
            
            except json.JSONDecodeError:
                await ws.send_json({"status": "error", "message": "Invalid JSON"})
        
        elif msg.type == WSMsgType.ERROR:
            print(f"WebSocket error: {ws.exception()}")
    
    return ws

app = web.Application()

# Routing
app.router.add_get("/", index)
app.router.add_get("/message.html", message_page)
app.router.add_post("/message", handle_message)
app.router.add_get("/ws", websocket_handler)

# Obsługa plików statycznych
app.router.add_static("/", path="front-init", name="static")

# Uruchomienie serwera HTTP
if __name__ == "__main__":
    web.run_app(app, host="localhost", port=3000)
