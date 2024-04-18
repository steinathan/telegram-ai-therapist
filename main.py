#!/usr/bin/env python3
import threading
import uvicorn

from fastapi import FastAPI

from dotenv import load_dotenv
from app.telegram_app.app import TelegramAgentApp


load_dotenv()

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


def run_server():
    uvicorn.run(app, host="0.0.0.0", port=1337)


def run_telegram_agent():
    app = TelegramAgentApp()
    app.run_until_complete()


if __name__ == "__main__":
    threading.Thread(target=run_server, daemon=True).start()
    run_telegram_agent()
