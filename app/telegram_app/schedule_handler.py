import asyncio
from datetime import datetime
import os
import random

from telegram import Bot

from app.db import chat_crud, user_crud
from app.db.models import Chat, User
from app.gpt.greeting_cron_generator import generate_greeting_message


def get_time_period(hour):
    if 5 <= hour < 12:
        return "Morning"
    elif 12 <= hour < 17:
        return "Afternoon"
    elif 17 <= hour < 20:
        return "Evening"
    else:
        return "Night"


def get_static_message() -> tuple[str, str]:
    remeber_messages = [
        "Keep in mind, I'm here for you 24/7. Feel free to share your problems with me anytime.",
        "Just a reminder, I'm available around the clock. Don't hesitate to reach out and talk about anything bothering you.",
        "Don't forget, I'm here whenever you need me, day or night. You can always confide in me.",
        "Just so you know, I'm here 24/7. You're welcome to come to me with any problems you have.",
        "I want you to know that I'm available 24/7. Feel free to reach out whenever you need someone to talk to.",
        "Just a heads up, I'm here for you 24/7. You can always share your problems with me.",
        "Keep in mind that I'm always available. If you ever need to talk or share your problems, I'm here.",
        "Just a quick reminder, I'm here round the clock. If you have any problems, you can always reach out to me.",
        "Just remember, I'm available anytime. Feel free to talk to me about anything that's on your mind.",
        "Just wanted to let you know, I'm here for you 24/7. Don't hesitate to come to me with any problems you have.",
        "I'm here to help you anytime, day or night. Feel free to share your concerns with me.",
        "No matter the time, I'm available to listen and help you with your problems.",
        "Day or night, I'm here for you. You can always count on me to listen and offer support.",
        "You're not alone. I'm here 24/7 to support you through anything you're going through.",
        "Anytime you need someone to talk to, I'm here. Don't hesitate to reach out.",
        "Remember, I'm just a message away whenever you need a listening ear.",
        "I'm here round the clock to support you. Feel free to reach out whenever you need to.",
        "No matter what time it is, you can always come to me with your problems.",
        "24 hours a day, 7 days a week, I'm here to lend a listening ear.",
        "You're never alone. I'm available anytime to help you work through your problems.",
    ]

    encouragements = [
        "You can do it! 💪",
        "Keep going! 🚀",
        "You're capable! 👍",
        "You've got what it takes! 💥",
        "You're unstoppable! 🌟",
        "Believe in yourself! 🌈",
        "Keep pushing! 🔥",
        "You're on the right track! 🛤️",
        "Don't give up! 🚫",
        "You're doing great! 👏",
        "Stay strong! 💪",
        "You're making progress! 📈",
        "Keep up the good work! 👍",
        "You're getting there! 🎯",
        "You're amazing! 😊",
        "You've got this in the bag! 🛍️",
        "You're a champion! 🏆",
        "You're on fire! 🔥",
        "You're almost there! 🏁",
        "You're a rockstar! 🌟",
    ]

    return (random.choice(remeber_messages), random.choice(encouragements))


def get_randint():
    return random.randint(5, 20)


async def greetings_job():
    bot = Bot(token=os.getenv("TELEGRAM_BOT_TOKEN", ""))
    async with bot:
        current_hour = datetime.now().hour
        day_period = get_time_period(current_hour)
        text = generate_greeting_message(day_period)

        users = user_crud.get_all()
        tasks = []

        async def __send_message(user: User):
            chat_id = user.real_id
            # if not chat_id == 1522427219:
            #     return

            print(f"Sending message to {user.full_name} with id {user.real_id}")
            (remeber_message, encouragment) = get_static_message()

            await bot.send_message(chat_id=chat_id, text=text)
            await asyncio.sleep(get_randint())

            await bot.send_message(
                chat_id=chat_id,
                text=remeber_message,
            )
            await asyncio.sleep(get_randint())
            await bot.send_message(
                chat_id=chat_id,
                text=encouragment,
            )

        for user in users:
            tasks.append(__send_message(user))
        asyncio.gather(*tasks)
