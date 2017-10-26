#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import Modules
import os
import time
import sys
import subprocess
from functools import wraps
from uuid import uuid4
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, \
    InlineQueryResultArticle, InputTextMessageContent
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, InlineQueryHandler


# Restrict Access
LIST_OF_ADMINS = [XXX]

# First, you have to create an Updater object. Replace 'TOKEN' with your Bot's API token.

updater = Updater(token='XXX')

# For quicker access to the Dispatcher used by your Updater, you can introduce it locally:

dispatcher = updater.dispatcher

# This is a good time to set up the logging module, so you will know when (and why)
# things don't work as expected:

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

# Now, you can define a function that should process a specific type of update:


def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I can help you manage your *Raspberry Pi*. Code is available at https://git.io/vd67s\n\nYou can control me by sending these commands:\n\n*List of Commands*\n/help - Prints this *Help*\n/ip - Prints *External IP*\n/menu - Shows inline *Menu*\n/restart - *Restarts* Bot\n/run - *Runs* a shell Command\n/who - *Who* is connected", parse_mode="MARKDOWN")


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)


def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="I can help you manage your *Raspberry Pi*. Code is available at https://git.io/vd67s\n\nYou can control me by sending these commands:\n\n*List of Commands*\n/help - Prints this *Help*\n/ip - Prints *External IP*\n/menu - Shows inline *Menu*\n/restart - *Restarts* Bot\n/run - *Runs* a shell Command\n/who - *Who* is connected", parse_mode="MARKDOWN")


'''
start - Starts Kenshō
help - Prints this Help
ip - Prints External IP
menu - Shows inline Menu
restart - Restarts Bot
run - Runs a shell Command
who - Who is connected
'''

start_handler = CommandHandler('help', help)
dispatcher.add_handler(start_handler)

# List of Functions


def restricted(func):
    @wraps(func)
    def wrapped(bot, update, *args, **kwargs):
        user_id = update.effective_user.id
        if user_id not in LIST_OF_ADMINS:
            print("Unauthorized access denied for {}.".format(user_id))
            return
        return func(bot, update, *args, **kwargs)
    return wrapped


@restricted
def restart(bot, update):
    bot.send_message(update.message.chat_id, "Bot is restarting...")
    time.sleep(0.2)
    os.execl(sys.executable, sys.executable, *sys.argv)


dispatcher.add_handler(CommandHandler('restart', restart))


@restricted
def who(bot, update):
    time.sleep(0.2)
    details = subprocess.check_output(['w'])
    bot.send_message(update.message.chat_id, details)


dispatcher.add_handler(CommandHandler('who', who))


@restricted
def run(bot, update, args):

    cmd = args[0].encode('utf8')
    counter = 1

    argsno = args.__len__()

    while counter < argsno:
        addcmd = ' ' + args[counter].encode('utf8')
        cmd = cmd + addcmd
        counter += 1

    details = subprocess.check_output(
        ['/usr/local/sbin/run.sh', 'bash', "%s" % cmd])
    bot.send_message(update.message.chat_id, details)
    print details


dispatcher.add_handler(CommandHandler('run', run, pass_args=True))


@restricted
def ip(bot, update):
    time.sleep(0.2)
    details = subprocess.check_output(['/usr/bin/curl', 'ipinfo.io'])
    bot.send_message(update.message.chat_id, details)


dispatcher.add_handler(CommandHandler('ip', ip))


def error(bot, update, error):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, error)


dispatcher.add_error_handler(error)


# Lets improve this with a menu

def menu(bot, update):
    keyboard = [[InlineKeyboardButton("IP", callback_data='ip'),
                 InlineKeyboardButton("Who", callback_data='who')],
                [InlineKeyboardButton(
                    "Run", switch_inline_query_current_chat='')],
                [InlineKeyboardButton("Help", callback_data='help')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose:', reply_markup=reply_markup)


dispatcher.add_handler(CommandHandler('menu', menu))


@restricted
def button(bot, update):
    query = update.callback_query
    time.sleep(0.2)
    details = subprocess.check_output(['/usr/local/sbin/run.sh', query.data])
    bot.edit_message_text(text="%s" % details,
                          chat_id=query.message.chat_id,
                          message_id=query.message.message_id,
                          parse_mode="MARKDOWN")


dispatcher.add_handler(CallbackQueryHandler(button))


@restricted
def inlinequery(bot, update):
    """Handle the inline query."""
    query = update.inline_query.query
    time.sleep(0.2)

    try:
        details = subprocess.check_output(query, shell=True)
        returncode = 0
    except subprocess.CalledProcessError as e:
        details = e.output
        returncode = e.returncode
    print (returncode)

    results = [
        InlineQueryResultArticle(
            id=uuid4(),
            title="Run",
            description="Runs a shell command on inline mode",
            input_message_content=InputTextMessageContent(details,
                                                          parse_mode="MARKDOWN"))]

    update.inline_query.answer(results)


dispatcher.add_handler(InlineQueryHandler(inlinequery))

# Start the Bot
updater.start_polling()

# Run the bot until the user presses Ctrl-C or the process receives SIGINT,
# SIGTERM or SIGABRT
updater.idle()
