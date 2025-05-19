from fastapi import FastAPI, Request

from RSA_module import RSA

app = FastAPI()


@app.post("/step0")
async def step0(request: Request):
    payload = await request.json()
    key_size = payload.get("key_size")
    index = payload.get("index")
    message = payload.get("message")