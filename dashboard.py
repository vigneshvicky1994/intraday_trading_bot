from fastapi import FastAPI, Request, WebSocket
from fastapi.templating import Jinja2Templates
import sqlite3
import datetime
from pathlib import Path

app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
DB_PATH = Path("app/trading.db")
active_websockets = []

@app.get("/")
def show_dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.websocket("/ws/updates")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    try:
        while True:
            await websocket.receive_text()
    except:
        active_websockets.remove(websocket)

async def broadcast_update(data: dict):
    for ws in active_websockets:
        await ws.send_json(data)
