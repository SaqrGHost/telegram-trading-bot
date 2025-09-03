"""Telegram bot interface."""
from __future__ import annotations
import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from utils.helpers import get_authorized_ids

logger = logging.getLogger(__name__)

autotrader_running = False


def _main_keyboard() -> InlineKeyboardMarkup:
    keyboard = [[InlineKeyboardButton("Start AutoTrader", callback_data="start")],
                [InlineKeyboardButton("Stop AutoTrader", callback_data="stop")],
                [InlineKeyboardButton("Balance", callback_data="balance")],
                [InlineKeyboardButton("Analyze Symbol", callback_data="analyze")]]
    return InlineKeyboardMarkup(keyboard)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.effective_user.id not in get_authorized_ids():
        await update.message.reply_text("Unauthorized")
        return
    await update.message.reply_text("Welcome to the trading bot", reply_markup=_main_keyboard())


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()
    global autotrader_running
    if query.data == "start":
        autotrader_running = True
        await query.edit_message_text("AutoTrader started")
    elif query.data == "stop":
        autotrader_running = False
        await query.edit_message_text("AutoTrader stopped")
    elif query.data == "balance":
        await query.edit_message_text("Balance feature not implemented")
    elif query.data == "analyze":
        await query.edit_message_text("Analysis feature not implemented")


def run_bot() -> None:
    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        logger.error("TELEGRAM_BOT_TOKEN not set")
        return
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    logger.info("Bot starting...")
    app.run_polling()
