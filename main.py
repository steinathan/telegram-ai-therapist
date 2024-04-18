#!/usr/bin/env python3
import threading
import uvicorn

from fastapi import FastAPI

from dotenv import load_dotenv
from app.telegram_app.app import telegram_app


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def main():
    uvicorn.run(app, host="0.0.0.0", port=1337)


if __name__ == "__main__":
    threading.Thread(target=main, daemon=True).start()
    telegram_app()
