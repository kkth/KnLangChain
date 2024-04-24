import uvicorn
from fastapi import FastAPI
from starlette.responses import StreamingResponse
import asyncio

app = FastAPI()


async def generate_data():
    for i in range(10):
        yield f"Data {i}\n"
        await asyncio.sleep(1)  # 模拟异步操作


@app.get("/stream")
async def stream_data():
    return StreamingResponse(generate_data())

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8009)