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
from app.gpt.chat import CompletionChat
from app.logging import logger
import logging

from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, Update
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Starts the conversation and asks the user about their gender."""
    assert update.message is not None

    reply_keyboard = [["Boy", "Girl", "Other"]]

    await update.message.reply_text(
        "Hi! My name is Professor Bot. I will hold a conversation with you. "
        "Send /cancel to stop talking to me.\n\n"
        "Are you a boy or a girl?",
        reply_markup=ReplyKeyboardMarkup(
            reply_keyboard,
            one_time_keyboard=True,
            input_field_placeholder="Boy or Girl?",
        ),
    )


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

    response = chat.forward(message=user_text, user=user)

    await update.message.reply_text(text=response)


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
    application.add_handler(
        handler=MessageHandler(filters=filters.ALL, callback=handle_message)
    )

    application.run_polling(allowed_updates=Update.ALL_TYPES)
