#!/usr/bin/python

# Import Modules
import os
import time
import sys
import subprocess
from functools import wraps
from telegram.ext import CommandHandler
from telegram.ext import Updater

# Restrict Access
LIST_OF_ADMINS = [423525222]

# First, you have to create an Updater object. Replace 'TOKEN' with your Bot's API token.

updater = Updater(token='473218049:AAH54a58sPKYKPtSC2_JfXWqIMMyAj8jvdg')

# For quicker access to the Dispatcher used by your Updater, you can introduce it locally:

dispatcher = updater.dispatcher

# This is a good time to set up the logging module, so you will know when (and why) things don't work as expected:

import logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',level=logging.INFO)

# Now, you can define a function that should process a specific type of update:

def start(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="Hey *Jose*, I'm your bot, please talk to me!", parse_mode='MARKDOWN')
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

def help(bot, update):
    bot.send_message(chat_id=update.message.chat_id, text="*List of Commands*\n/help - Prints this *Help*\n/ip - Prints *External IP*\n/restart - *Restarts* Bot\n/run - *Runs* a Command\n/start - *Hello* Message\n/who - *Who* is connected", parse_mode="MARKDOWN")
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
    time.sleep(0.2)
    details = subprocess.check_output(args)
    bot.send_message(update.message.chat_id, details)
dispatcher.add_handler(CommandHandler('run', run, pass_args=True))

@restricted
def ip(bot, update):
    time.sleep(0.2)
    details = subprocess.check_output(['/usr/bin/curl', 'ipinfo.io'])
    bot.send_message(update.message.chat_id, details)

dispatcher.add_handler(CommandHandler('ip', ip))

# And that's all you need. To start the bot, run:
updater.start_polling()
updater.idle()
