#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.

First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.

Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import json
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram.update import Update

# Enable logging
from LinuxServerStatsTelegramBot.DI import DI
from LinuxServerStatsTelegramBot.commmand.CronStats import CronStats
from LinuxServerStatsTelegramBot.commmand.DateAndLocation import DateAndLocation
from LinuxServerStatsTelegramBot.commmand.DiskStats import DiskStats
from LinuxServerStatsTelegramBot.commmand.DockerStats import DockerStats
from LinuxServerStatsTelegramBot.commmand.MemoryStats import MemoryStats
from LinuxServerStatsTelegramBot.core.Invoker import Invoker
from LinuxServerStatsTelegramBot.sender.TelegramSender import TelegramSender

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)

logger = logging.getLogger(__name__)


# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    logger.info(f"Received command start with {update} in the context: {context}")
    update.message.reply_text("Hi!")


def help(update, context):
    """Send a message when the command /help is issued."""
    print(update)
    print(context)
    update.message.reply_text("Help!")


def memory(update, context):
    """Send a message when the command /help is issued."""
    chat_id = update.message.from_user.id
    DI.set_sender(TelegramSender(str(chat_id)))
    Invoker.send_data_as_image(MemoryStats())
    update.message.reply_text("Sending memory stats")


def dateandlocation(update, context):
    """Send a message when the command /help is issued."""
    chat_id = update.message.from_user.id
    DI.set_sender(TelegramSender(str(chat_id)))
    Invoker.send_data_as_image(DateAndLocation())
    update.message.reply_text("Sending memory stats")


def cron(update, context):
    """Send a message when the command /help is issued."""
    chat_id = update.message.from_user.id
    DI.set_sender(TelegramSender(str(chat_id)))
    Invoker.send_data_as_image(CronStats())
    update.message.reply_text("Sending memory stats")


def disk(update, context):
    """Send a message when the command /help is issued."""
    chat_id = update.message.from_user.id
    DI.set_sender(TelegramSender(str(chat_id)))
    Invoker.send_data_as_image(DiskStats())
    update.message.reply_text("Sending memory stats")


def docker(update, context):
    """Send a message when the command /help is issued."""
    chat_id = update.message.from_user.id
    DI.set_sender(TelegramSender(str(chat_id)))
    Invoker.send_data_as_image(DockerStats())
    update.message.reply_text("Sending memory stats")


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("5216070097:AAFvhhKgrB5Ct8YP6xN0Mne8dFwl8pitCW0", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("memory", memory))
    dp.add_handler(CommandHandler("dateandlocation", dateandlocation))
    dp.add_handler(CommandHandler("cron", cron))
    dp.add_handler(CommandHandler("disk", disk))
    dp.add_handler(CommandHandler("docker", docker))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == "__main__":
    main()
