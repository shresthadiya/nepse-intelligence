from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from typing import List

router = APIRouter(tags=["WebSocket"])


class ConnectionManager:

    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        disconnected = []

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception:
                disconnected.append(connection)

        for connection in disconnected:
            self.disconnect(connection)


manager = ConnectionManager()


@router.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        await websocket.send_json({
            "type": "connection",
            "message": "Connected to NEPSE Intelligence live updates"
        })

        while True:
            # Keep connection alive and receive client messages.
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)

    except Exception:
        manager.disconnect(websocket)