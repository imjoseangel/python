#!/usr/bin/env python

import telebot
TOKEN = '108270433:AAHGe0GZv4dqla-m4l07IgiNhhRBGsdkyWQ'
bot = telebot.TeleBot(TOKEN)

# Handle /start and /help
@bot.message_handler(commands=['start', 'help'])
def command_help(message):
    bot.reply_to(message, "Hello, did someone call for help?")

# Handles all messages which text matches the regex regexp.
# See https://en.wikipedia.org/wiki/Regular_expression
# This regex matches all sent url's.
@bot.message_handler(regexp='((https?):((//)|(\\\\))+([\w\d:#@%/;$()~_?\+-=\\\.&](#!)?)*)')
def command_url(message):
    bot.reply_to(message, "I shouldn't open that url, should I?")

# Handle all sent documents of type 'text/plain'.
@bot.message_handler(func=lambda message: message.document.mime_type == 'text/plain', content_types=['document'])
def command_handle_document(message):
    bot.reply_to(message, "Document received, sir!")

# Default command handler. A lambda expression which always returns True is used for this purpose.
@bot.message_handler(func=lambda message: True, content_types=['audio', 'video', 'document', 'text', 'location', 'contact', 'sticker'])
def default_command(message):
    bot.reply_to(message, "This is the default command handler.")

bot.polling()

while True: # Don't end the main thread.
    pass
