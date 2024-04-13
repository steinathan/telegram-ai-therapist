#!/usr/bin/env python


from dotenv import load_dotenv
from app.telegram_app.app import telegram_app

load_dotenv()


if __name__ == "__main__":
    telegram_app()
