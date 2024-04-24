from telegram import Bot


async def greet_everyone(bot: Bot):
    await bot.send_message(1522427219, "Hello, everyone!")
