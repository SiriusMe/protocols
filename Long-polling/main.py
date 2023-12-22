from fastapi import FastAPI
import asyncio

app = FastAPI()


class LongPollingManager:
    def __init__(self):
        self.queue = asyncio.Queue()

    async def wait_for_update(self):
        return await self.queue.get()

    def send_update(self, data):
        self.queue.put_nowait(data)


long_polling_manager = LongPollingManager()


@app.get("/poll")
async def poll_for_updates():
    result = await long_polling_manager.wait_for_update()
    return {"update": result}


@app.post("/send-update")
async def send_update(data: dict):
    long_polling_manager.send_update(data)
    return {"message": "Update sent successfully"}

# uvicorn main:app --host 172.18.100.240 --port 8999
