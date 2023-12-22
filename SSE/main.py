import random as rand
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
import asyncio

app = FastAPI()

clients = []

# Serve static files from the "static" directory
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/sse")
async def sse(request: Request):
    response = StreamingResponse(
        sse_generator(),
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
    )
    response.headers["Access-Control-Allow-Origin"] = "*"
    return response


# a generator function for sending SSE events
async def sse_generator():
    client = Client()
    clients.append(client)
    try:
        while True:
            # Generate a random float between 10 and 200 using the rand module
            random_float = rand.uniform(10, 200)
            # Send the random float as an SSE event
            yield f"data: {random_float:.2f}\n\n"
            await asyncio.sleep(5)
    except asyncio.CancelledError:
        clients.remove(client)


# a class to represent clients
class Client:
    def __init__(self):
        self.message_queue = asyncio.Queue()


@app.post("/send_message")
async def send_message(message: str):
    for client in clients:
        await client.message_queue.put(message)
    return {"message": "Message sent to all clients"}

# uvicorn main:app --reload --host 172.18.100.240 --port 8989
