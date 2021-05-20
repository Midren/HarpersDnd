import json

import telebot

creds = json.load(open('credentials.json'))
bot = telebot.TeleBot(creds['token'], parse_mode='html')
