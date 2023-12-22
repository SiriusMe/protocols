from fastapi import FastAPI, WebSocket
from starlette.middleware.cors import CORSMiddleware
import asyncio
import random

from starlette.websockets import WebSocketDisconnect

app = FastAPI()

# Add CORS middleware to allow connections from any origin
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# List to store WebSocket clients
clients = []


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Accept the WebSocket connection
    await websocket.accept()

    # Add the WebSocket client to the list
    clients.append(websocket)

    try:
        while True:
            # Generate a random float between 10 and 200
            random_float = random.uniform(10, 200)

            # Send the random float as a WebSocket message to all connected clients
            for client in clients:
                await client.send_text(f""
                                       f"{random_float:.2f}")

            # Wait for a few seconds before sending the next random float
            await asyncio.sleep(5)
    except WebSocketDisconnect:
        # Remove the WebSocket client from the list when disconnected
        clients.remove(websocket)
#uvicorn main:app --host 172.18.100.240 --port 8000