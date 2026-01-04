from typing import Union
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

from .config import log


app = FastAPI()
log.info("FastAPI application instance created.")

# Not safe! Add your own allowed domains
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TypePayload(BaseModel):
    content: str

# Example GET route for app


@app.get("/")
def read_root():
    return {"Message": "Hello World! FastAPI is working."}

# Example POST route for app


@app.post("/getdata")
async def create_secret(payload: TypePayload):
    with open('output_file.txt', 'a') as f:
        now = datetime.now()
        formatted_date = now.strftime("%B %d, %Y at %I:%M %p")
        f.write(formatted_date + ": " + payload.content)
        f.write('\n')
    return payload.content
