#!/usr/bin/env python
# pylint: disable=unused-argument
# This program is dedicated to the public domain under the CC0 license.

"""
First, a few callback functions are defined. Then, those functions are passed to
the Application and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Example of a bot-user conversation using ConversationHandler.
Send /start to initiate the conversation.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import os
from app.exceptions import UpgradeRequiredException
from app.gpt.chat import CompletionChat
from app.logging import logger

from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    Update,
)
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)

from app.db import User, user_crud

chat = CompletionChat()

start_message = """
🧠 Introducing the first AI mental health coach, available 24/7.

✅ Reframe negative thoughts
✅ Take actionable steps to overcome challenges
✅ Emphasize physical fitness for mental well-being
✅ Provide support throughout your day
✅ Offer encouragement to uplift your mood

You can:
🎤 Send voice messages for responses in audio
💬 Send chat messages for text responses
📸 Share photos for analysis
🔎 Send web URLs for summarization


💡 Feedback:
Have suggestions, ideas, or encountered bugs? Share them with us at https://linkedin.com/in/navicstein.
"""

upgrade_message = f"""To continue our conversation, please select "Continue talking" below.

{start_message}
"""


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the conversation and asks you about your email to get started."""
    assert update.message is not None

    # TODO: ask the user about thier email address
    await update.message.reply_text(
        start_message,
    )


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Resets the conversation, deleting the previous user's messages."""
    assert update.message is not None

    # TODO: implement this
    await update.message.reply_text(
        "I've deleted your messages in my histoy, you may as well clear the history from telegram itself.",
    )


async def billing(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Download all your invoices."""
    assert update.message is not None

    # TODO: implement this

    keyboard = [
        [
            InlineKeyboardButton(
                "⏬ Download invoices",
                url="https://linkedin.com/in/navicstein",
            ),
            InlineKeyboardButton(
                "🚫 Cancel Subscription",
                url="https://linkedin.com/in/navicstein",
            ),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Choose an option:", reply_markup=reply_markup)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handles the user message"""
    if not update.message:
        return

    assert update.effective_user is not None

    # TODO: implement this
    if update.message.audio or update.message.voice:
        await update.message.reply_text(
            text="Sorry, i can't listen to audio notes at the moment"
        )
        return

    user_text = update.message.text
    if not user_text:
        return

    user = user_crud.get(update.effective_user.id)
    if not user:
        user = user_crud.create(
            User(
                id=update.effective_user.id,
                full_name=update.effective_user.full_name,
                telegram_id=update.effective_user.id,
            )
        )

    try:
        response = chat.forward(message=user_text, user=user)
        await update.message.reply_text(text=response)
    except UpgradeRequiredException:
        keyboard = [
            [
                InlineKeyboardButton(
                    # TODO: add payment link
                    "🔥Continue Talking",
                    url="https://linkedin.com/in/navicstein",
                )
            ],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(text=upgrade_message, reply_markup=reply_markup)
    except Exception as e:
        logger.exception(e, exc_info=True)
        await update.message.reply_text(
            text="I'm sorry, I could'nt process your last message, can you resend it?"
        )


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Cancels and ends the conversation."""
    assert update.message is not None, "update.message is None in cancel()"

    user = update.message.from_user
    logger.info("User %s canceled the conversation.", user.first_name)  # type: ignore
    await update.message.reply_text(
        "Bye! I hope we can talk again some day.", reply_markup=ReplyKeyboardRemove()
    )

    return ConversationHandler.END


def telegram_app() -> None:
    """Run the bot."""
    application = (
        Application.builder().token(os.getenv("TELEGRAM_BOT_TOKEN", "")).build()
    )

    application.add_handler(handler=CommandHandler(command="start", callback=start))
    application.add_handler(handler=CommandHandler(command="reset", callback=reset))
    application.add_handler(handler=CommandHandler(command="billing", callback=billing))
    application.add_handler(
        handler=MessageHandler(filters=filters.ALL, callback=handle_message)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
